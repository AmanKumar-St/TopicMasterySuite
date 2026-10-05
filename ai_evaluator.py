"""
AIEvaluator: Robust OpenRouter Free-Tier & CodeCraft Multi-Model Router.
Features automated model cascading, rate-limit failovers, topic analysis,
and structured pedagogical evaluation.
"""

import json
import os
import re
import time
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error
import yaml


class AIEvaluator:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

        self.openrouter_key = os.environ.get(
            "OPENROUTER_API_KEY",
            self.config.get("ai_backend", {}).get("openrouter", {}).get("api_key", "")
        )
        self.openrouter_base = self.config.get("ai_backend", {}).get("openrouter", {}).get("base_url", "https://openrouter.ai/api/v1")
        self.openrouter_models = self.config.get("ai_backend", {}).get("openrouter", {}).get("models", [
            "qwen/qwen3.8-27b:free",
            "google/gemma-4-31b-it:free",
            "nvidia/nemotron-3.5-lightning:free",
            "cohere/north-mini-code:free",
            "openrouter/free"
        ])

        self.codecraft_key = os.environ.get(
            "CODECRAFT_API_KEY",
            self.config.get("ai_backend", {}).get("codecraft", {}).get("api_key", "")
        )
        self.codecraft_base = self.config.get("ai_backend", {}).get("codecraft", {}).get("base_url", "https://api.codecraft.ai/v1")

        eval_cfg = self.config.get("evaluation", {})
        self.temperature = eval_cfg.get("temperature", 0.1)
        self.max_tokens = eval_cfg.get("max_tokens", 1500)
        self.passing_score = eval_cfg.get("passing_score", 70)
        self.partial_score_min = eval_cfg.get("partial_score_min", 40)

    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                pass
        return {}

    def _call_openrouter(self, model: str, system_prompt: str, user_prompt: str) -> Optional[str]:
        url = f"{self.openrouter_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.openrouter_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://localhost",
            "X-Title": "LearningExercises"
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            # 429 Rate limit or 5xx server error
            err_body = ""
            try:
                err_body = e.read().decode("utf-8")
            except Exception:
                pass
            print(f"[OpenRouter Router] Model {model} returned HTTP {e.code}: {e.reason} -> Trying next model in cascade...")
            return None
        except Exception as e:
            print(f"[OpenRouter Router] Model {model} request error: {e} -> Trying next model in cascade...")
            return None

    def _call_codecraft(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        if not self.codecraft_key or self.codecraft_key.startswith("${"):
            return None

        url = f"{self.codecraft_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.codecraft_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "codecraft-coder-v1",
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except Exception as e:
            print(f"[CodeCraft Fallback] Request error: {e}")
            return None

    def chat_complete(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """
        Executes a prompt across the priority chain of free models with auto-failover.
        """
        # Try OpenRouter Free Models Cascade
        for model in self.openrouter_models:
            content = self._call_openrouter(model, system_prompt, user_prompt)
            if content:
                return content
            time.sleep(0.3)

        # Try CodeCraft Fallback
        cc_content = self._call_codecraft(system_prompt, user_prompt)
        if cc_content:
            return cc_content

        return None

    def parse_json_response(self, text: Optional[str]) -> Dict[str, Any]:
        """
        Robustly extracts JSON from LLM response text even with surrounding markdown.
        """
        if not text:
            return {}

        # Strip markdown ```json ... ``` codeblocks
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        # Try searching for raw { ... }
        match_raw = re.search(r"(\{.*\})", text, re.DOTALL)
        if match_raw:
            try:
                return json.loads(match_raw.group(1))
            except Exception:
                pass

        try:
            return json.loads(text)
        except Exception:
            return {}

    def analyze_topic(self, topic_input: str) -> Dict[str, Any]:
        """
        Analyzes the topics entered by the student at the beginning of the notebook.
        Generates core learning pillars, pitfalls, and diagnostic checklist.
        """
        system_prompt = (
            "You are a master JavaScript instructor. "
            "Analyze the user's input topic(s) and provide a structured JSON curriculum diagnosis. "
            "Return ONLY a JSON object, no conversational filler."
        )
        user_prompt = f"""
TOPIC(S) ENTERED BY USER:
{topic_input}

Return JSON with this schema:
{{
  "topic_summary": "Brief 1-sentence synthesis of the subject matter",
  "key_mental_models": ["Core concept 1", "Core concept 2", "Core concept 3"],
  "common_pitfalls": ["Pitfall 1 (e.g. lost this context)", "Pitfall 2 (e.g. arguments vs rest)"],
  "mastery_checklist": ["What you must master 1", "What you must master 2"],
  "recommended_focus": "Advice for tackling the 10 diagnostic test questions"
}}
"""
        response_text = self.chat_complete(system_prompt, user_prompt)
        parsed = self.parse_json_response(response_text)
        if not parsed or "topic_summary" not in parsed:
            parsed = {
                "topic_summary": f"In-depth analysis for: {topic_input or 'JavaScript Decorators & call/apply'}",
                "key_mental_models": [
                    "Runtime Context vs Lexical Scope ('this' binding)",
                    "Function Decorators as Transparent Higher-Order Wrappers",
                    "Argument Forwarding via Rest Parameters (...args) & apply()"
                ],
                "common_pitfalls": [
                    "Detached method invocation losing original object context",
                    "Arrow functions capturing outer lexical this rather than call-site context",
                    "Overwriting original function properties and metadata during decoration"
                ],
                "mastery_checklist": [
                    "Master func.call(this, ...args) and func.apply(this, args)",
                    "Implement transparent caching, debouncing, and throttling wrappers",
                    "Handle function composition order (right-to-left onion model)",
                    "Preserve property descriptors via Object.getOwnPropertyDescriptors"
                ],
                "recommended_focus": "Ensure all wrappers capture `this` dynamically with regular functions and forward all arguments cleanly."
            }
        return parsed

    def evaluate_question(
        self,
        question_id: int,
        question_title: str,
        question_desc: str,
        expected_concepts: List[str],
        student_code: str,
        test_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluates a student's answer code and test execution results to produce a comprehensive score & feedback.
        """
        total_tests = test_results.get("total", 0)
        passed_tests = test_results.get("passed", 0)
        failed_tests = test_results.get("failed", 0)
        all_passed = (total_tests > 0 and failed_tests == 0 and not test_results.get("error"))

        system_prompt = (
            "You are an expert JavaScript mentor. Evaluate the student's solution based on code quality, "
            "conceptual understanding of JavaScript decorators, call/apply, closures, and the test run results. "
            "Return ONLY valid JSON."
        )

        user_prompt = f"""
QUESTION #{question_id}: {question_title}
DESCRIPTION & REQUIREMENTS:
{question_desc}

KEY CONCEPTS TESTED:
{', '.join(expected_concepts)}

STUDENT SUBMISSION CODE:
```javascript
{student_code}
```

DETERMINISTIC TEST RESULTS:
- Total Tests: {total_tests}
- Passed Tests: {passed_tests}
- Failed Tests: {failed_tests}
- Test Details: {json.dumps(test_results.get('tests', []), indent=2)}
- Runtime Logs: {json.dumps(test_results.get('logs', []), indent=2)}
- Error (if any): {test_results.get('error', 'None')}

TASK:
Evaluate the answer. If all deterministic tests passed and code is clean, award full marks (90-100).
If tests failed or code has anti-patterns, award appropriate partial (40-69) or failing (<40) score with clear pedagogical explanation.

Return ONLY a JSON object:
{{
  "verdict": "correct" | "partially_correct" | "incorrect",
  "score": <integer 0-100>,
  "explanation": "<2-3 sentence assessment of the code>",
  "key_insight": "<The core JavaScript concept>",
  "next_steps": "<1-2 actionable tips>"
}}
"""
        response_text = self.chat_complete(system_prompt, user_prompt)
        res = self.parse_json_response(response_text)

        # Fallback / validation against deterministic test execution
        if "score" not in res or not isinstance(res["score"], (int, float)):
            if all_passed:
                res["score"] = 100
                res["verdict"] = "correct"
                res["explanation"] = "Outstanding work! All unit tests and assertion checks passed cleanly."
                res["key_insight"] = f"Correct implementation of {expected_concepts[0]}."
                res["next_steps"] = "Proceed to the next challenge."
            elif passed_tests > 0:
                res["score"] = int((passed_tests / max(total_tests, 1)) * 80)
                res["verdict"] = "partially_correct"
                failed_names = [t.get("name") for t in test_results.get("tests", []) if not t.get("passed")]
                res["explanation"] = f"Passed {passed_tests}/{total_tests} tests. Failed checks: {', '.join(failed_names)}."
                res["key_insight"] = "Check edge cases and context forwarding."
                res["next_steps"] = "Review the hints and address the failing assertion conditions."
            else:
                res["score"] = 25
                res["verdict"] = "incorrect"
                err_msg = test_results.get("error") or "Tests did not pass."
                res["explanation"] = f"Code failed execution or assertion tests: {err_msg}"
                res["key_insight"] = f"Review requirements for {expected_concepts[0]}."
                res["next_steps"] = "Consult Hint 1 and Hint 2 to refine your approach."

        if "verdict" not in res:
            res["verdict"] = "correct" if res["score"] >= self.passing_score else ("partially_correct" if res["score"] >= self.partial_score_min else "incorrect")

        return res
