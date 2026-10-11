"""
Topic Mastery Engine
====================
A fully dynamic, LLM-powered practice engine for Jupyter notebooks.

- No hardcoded questions. No templates. No deterministic answers.
- Every question is generated fresh by an LLM and evaluated by an LLM.
- Auto-detects whichever LLM provider you have configured:
  OpenRouter  ->  GEMINI  ->  OpenAI  ->  local Ollama.

Environment variables (put them in a `.env` file next to the notebook):
    OPENROUTER_API_KEY=sk-or-v1-...
    GEMINI_API_KEY=...            (or GOOGLE_API_KEY)
    OPENAI_API_KEY=sk-...
    # Ollama needs no key - just have it running locally (ollama serve)
"""

from __future__ import annotations

import json
import os
import random
import re
from difflib import SequenceMatcher
from pathlib import Path

import requests

try:  # optional convenience - works fine without it
    from dotenv import load_dotenv

    load_dotenv()
except Exception:
    pass

HISTORY_FILE = Path(".topic_mastery_history.json")

# Free-model fallback chain for OpenRouter (tried in order on failure)
OPENROUTER_MODELS = [
    "openrouter/free",
    "meta-llama/llama-3.3-70b-instruct:free",
    "google/gemma-3-27b-it:free",
    "qwen/qwen3-32b:free",
]


class LLMError(RuntimeError):
    """Raised when no LLM provider is reachable or all calls fail."""


# --------------------------------------------------------------------------- #
#  LLM client (auto-detecting, provider-agnostic)
# --------------------------------------------------------------------------- #
class LLMClient:
    def __init__(self, model: str | None = None, temperature: float = 0.9):
        self.temperature = temperature
        self.provider, self.model, self._key = self._detect(model)

    # ---- provider detection ------------------------------------------------ #
    def _detect(self, model: str | None):
        if key := os.getenv("OPENROUTER_API_KEY"):
            return "openrouter", model or OPENROUTER_MODELS[0], key
        if key := (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
            return "gemini", model or "gemini-2.0-flash", key
        if key := os.getenv("OPENAI_API_KEY"):
            return "openai", model or "gpt-4o-mini", key
        # last resort: a locally running Ollama instance
        try:
            r = requests.get("http://localhost:11434/api/tags", timeout=2)
            if r.ok:
                models = [m["name"] for m in r.json().get("models", [])]
                if models:
                    return "ollama", model or models[0], None
        except requests.RequestException:
            pass
        raise LLMError(
            "No LLM provider found. Set one of OPENROUTER_API_KEY / "
            "GEMINI_API_KEY / OPENAI_API_KEY in a .env file, or run Ollama locally."
        )

    # ---- unified chat interface ------------------------------------------- #
    def chat(self, messages: list[dict], temperature: float | None = None) -> str:
        temp = self.temperature if temperature is None else temperature
        if self.provider == "gemini":
            return self._gemini(messages, temp)
        return self._openai_compatible(messages, temp)

    def _openai_compatible(self, messages, temperature) -> str:
        urls = {
            "openrouter": "https://openrouter.ai/api/v1/chat/completions",
            "openai": "https://api.openai.com/v1/chat/completions",
            "ollama": "http://localhost:11434/v1/chat/completions",
        }
        candidates = (
            OPENROUTER_MODELS if self.provider == "openrouter" else [self.model]
        )
        last_err = None
        for mdl in candidates:
            try:
                headers = {"Content-Type": "application/json"}
                if self._key:
                    headers["Authorization"] = f"Bearer {self._key}"
                r = requests.post(
                    urls[self.provider],
                    headers=headers,
                    json={
                        "model": mdl,
                        "messages": messages,
                        "temperature": temperature,
                    },
                    timeout=120,
                )
                if r.status_code == 429 or r.status_code >= 500:
                    last_err = f"{mdl}: HTTP {r.status_code}"
                    continue  # try next free model
                r.raise_for_status()
                self.model = mdl
                return r.json()["choices"][0]["message"]["content"]
            except requests.RequestException as e:
                last_err = f"{mdl}: {e}"
                continue
        raise LLMError(f"All model attempts failed. Last error: {last_err}")

    def _gemini(self, messages, temperature) -> str:
        prompt = "\n\n".join(
            f"[{m['role'].upper()}]\n{m['content']}" for m in messages
        )
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model}:generateContent?key={self._key}"
        )
        r = requests.post(
            url,
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"temperature": temperature},
            },
            timeout=120,
        )
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]


# --------------------------------------------------------------------------- #
#  helpers
# --------------------------------------------------------------------------- #
def _extract_json(text: str) -> dict:
    """Robustly pull the first JSON object out of an LLM reply."""
    text = re.sub(r"```(?:json)?", "", text).strip()
    start, depth = text.find("{"), 0
    if start == -1:
        raise LLMError(f"LLM did not return JSON:\n{text[:400]}")
    for i in range(start, len(text)):
        if text[i] == "{":
            depth += 1
        elif text[i] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(text[start : i + 1])
    raise LLMError(f"Incomplete JSON from LLM:\n{text[:400]}")


def _similar(a: str, b: str) -> float:
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()


# --------------------------------------------------------------------------- #
#  the engine
# --------------------------------------------------------------------------- #
class MasteryEngine:
    """Stateful engine: one instance = one practice session (history persists)."""

    def __init__(self, client: LLMClient | None = None):
        self.client = client or LLMClient()
        self.topic: str | None = None
        self.analysis: dict | None = None
        self.current_question: dict | None = None
        self.results: list[dict] = []
        self.history: dict = self._load_history()

    # ---- persistence ------------------------------------------------------- #
    @staticmethod
    def _load_history() -> dict:
        if HISTORY_FILE.exists():
            try:
                return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                return {}
        return {}

    def _save_history(self):
        HISTORY_FILE.write_text(
            json.dumps(self.history, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    def _past_questions(self) -> list[str]:
        if not self.topic:
            return []
        return self.history.get(self.topic.lower(), {}).get("questions", [])

    # ---- step 1: topic analysis ------------------------------------------- #
    def analyze_topic(self, topic: str, clarification: str | None = None) -> dict:
        ctx = f'\nThe user already clarified: "{clarification}"' if clarification else ""
        raw = self.client.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "You are an expert curriculum analyst. Analyze the topic a "
                        "learner says they just studied. Reply ONLY with a JSON object."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""Topic entered by learner: "{topic}"{ctx}

Return JSON with exactly these keys:
{{
  "refined_topic": "a precise, well-scoped version of the topic",
  "subject": "the subject area, e.g. 'Physics', 'World History', 'Python programming'",
  "domain": "broader domain, e.g. 'Natural Sciences', 'Computer Science'",
  "is_code_topic": true/false,
  "scope_summary": "one sentence describing what a quiz on this topic should cover",
  "is_ambiguous": true/false,
  "clarifying_questions": ["..."]
}}

Rules:
- Set is_ambiguous=true ONLY if the topic is too broad or vague to write focused
  practice questions (e.g. "science", "programming", "history", "math").
- If ambiguous, provide 2-4 specific clarifying questions that would narrow it down.
- If the topic is already specific enough (e.g. "Python decorators",
  "the French Revolution", "Bayes' theorem"), set is_ambiguous=false and
  clarifying_questions=[].""",
                },
            ],
            temperature=0.3,
        )
        return _extract_json(raw)

    def set_topic(self, topic: str, analysis: dict):
        self.topic = analysis.get("refined_topic") or topic
        self.analysis = analysis
        self.history.setdefault(self.topic.lower(), {"questions": []})
        self._save_history()

    # ---- step 2: dynamic question generation ------------------------------- #
    def ask_question(self, difficulty: str = "auto") -> dict:
        if not self.topic:
            raise LLMError("No topic set. Run the topic cell first.")
        past = self._past_questions()
        avoid = "\n".join(f"- {q}" for q in past[-25:]) or "- (none yet)"
        nonce = random.randint(100_000, 999_999)
        asked = len(past)

        system = (
            "You are a master examiner creating ONE unique practice question. "
            "Reply ONLY with a JSON object."
        )
        user = f"""Topic: {self.topic}
Subject: {self.analysis.get('subject', 'general')}
Question number in this session: {asked + 1}
Requested difficulty: {difficulty} (if "auto", ramp difficulty as the session progresses)
Creativity nonce: {nonce} (use it to vary angle, scenario, and phrasing - NEVER reuse a past angle)

Questions already asked in this topic - do NOT repeat or paraphrase any of them:
{avoid}

Return JSON with exactly these keys:
{{
  "question": "the question text (may include a scenario or a short code snippet if the subject is a programming language)",
  "type": "one of: conceptual | application | code-writing | debugging | analysis",
  "difficulty": "easy | medium | hard",
  "expected_concepts": ["the key ideas a correct answer must demonstrate"]
}}"""

        question = None
        for _ in range(3):  # retry until it's genuinely new
            data = _extract_json(self.client.chat(
                [{"role": "system", "content": system},
                 {"role": "user", "content": user}]
            ))
            if not any(_similar(data["question"], p) > 0.75 for p in past):
                question = data
                break
        question = question or data  # accept last attempt even if similar

        self.history[self.topic.lower()]["questions"].append(question["question"])
        self._save_history()
        self.current_question = question
        return question

    def get_hint(self) -> str:
        if not self.current_question:
            raise LLMError("No active question. Run new_question() first.")
        return self.client.chat(
            [
                {"role": "system", "content": "You are a Socratic tutor. Give ONE hint that nudges the learner toward the answer WITHOUT revealing it. 2-3 sentences max."},
                {"role": "user", "content": f"Topic: {self.topic}\nQuestion: {self.current_question['question']}"},
            ],
            temperature=0.7,
        )

    # ---- step 3: AI answer evaluation -------------------------------------- #
    def evaluate(self, answer: str) -> dict:
        if not self.current_question:
            raise LLMError("No active question. Run new_question() first.")
        q = self.current_question
        raw = self.client.chat(
            [
                {
                    "role": "system",
                    "content": (
                        "You are a fair, encouraging examiner grading a learner's "
                        "answer. Judge the SUBSTANCE, not the wording. Reply ONLY "
                        "with a JSON object."
                    ),
                },
                {
                    "role": "user",
                    "content": f"""Topic: {self.topic}
Question: {q['question']}
Expected concepts: {json.dumps(q.get('expected_concepts', []))}

Learner's answer:
\"\"\"
{answer}
\"\"\"

Return JSON with exactly these keys:
{{
  "verdict": "correct | partially_correct | incorrect",
  "score": 0-10,
  "feedback": "what was right, what was wrong or missing, and why (2-5 sentences)",
  "model_answer": "a complete, ideal answer the learner can study",
  "key_points_missed": ["concepts the learner missed, empty if none"]
}}

Grading rules:
- correct: demonstrates essentially all expected concepts.
- partially_correct: some concepts right, important ones missing or wrong.
- incorrect: fundamentally wrong, empty, or off-topic.
- For code answers, judge correctness of logic, not style.""",
                },
            ],
            temperature=0.3,
        )
        result = _extract_json(raw)
        result["question"] = q["question"]
        result["your_answer"] = answer
        self.results.append(result)
        return result

    # ---- session summary ---------------------------------------------------- #
    def summary(self) -> dict:
        if not self.results:
            return {"attempted": 0}
        scores = [r.get("score", 0) for r in self.results]
        return {
            "attempted": len(self.results),
            "correct": sum(1 for r in self.results if r.get("verdict") == "correct"),
            "partially_correct": sum(1 for r in self.results if r.get("verdict") == "partially_correct"),
            "incorrect": sum(1 for r in self.results if r.get("verdict") == "incorrect"),
            "average_score": round(sum(scores) / len(scores), 1),
        }
