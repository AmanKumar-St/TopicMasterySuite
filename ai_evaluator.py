"""
AIEvaluator: Robust OpenRouter Free-Tier & CodeCraft Multi-Model Router.
Features:
- Automated dynamic question generation for ANY topic based on plan.md's 10-tier pattern
- Autonomous backend evaluation without exposing boilerplate to user
- Multi-model cascading failover across top free models
"""

import json
import os
import re
import time
from typing import Any, Dict, List, Optional
import urllib.request
import urllib.error
import yaml
from dotenv import load_dotenv

load_dotenv()


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
            "openrouter/free",
            "qwen/qwen3.8-27b:free"
        ])

        self.codecraft_key = os.environ.get(
            "CODECRAFT_API_KEY",
            self.config.get("ai_backend", {}).get("codecraft", {}).get("api_key", "")
        )
        self.codecraft_base = self.config.get("ai_backend", {}).get("codecraft", {}).get("base_url", "https://api.codecraft.ai/v1")

        self.runinfra_key = os.environ.get(
            "RUNINFRA_GATEWAY_KEY",
            self.config.get("ai_backend", {}).get("runinfra", {}).get("api_key", "")
        )
        self.runinfra_base = self.config.get("ai_backend", {}).get("runinfra", {}).get("base_url", "https://api.runinfra.ai/v1")
        self.runinfra_models = self.config.get("ai_backend", {}).get("runinfra", {}).get("models", [
            "glm-5-3-flash"
        ])

        eval_cfg = self.config.get("evaluation", {})
        self.temperature = eval_cfg.get("temperature", 0.1)
        self.max_tokens = eval_cfg.get("max_tokens", 2500)
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

    def _call_openrouter(self, model: str, system_prompt: str, user_prompt: str, max_tokens: Optional[int] = None) -> Optional[str]:
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
            "max_tokens": max_tokens or self.max_tokens
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choice = data.get("choices", [{}])[0]
                msg = choice.get("message", {})
                content = msg.get("content")
                if not content:
                    content = msg.get("reasoning")
                if not content and "reasoning_details" in msg:
                    details = msg.get("reasoning_details", [])
                    if details and isinstance(details, list) and len(details) > 0 and "text" in details[0]:
                        content = details[0]["text"]
                return content
        except Exception:
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
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                return data["choices"][0]["message"]["content"]
        except Exception:
            return None

    def _call_runinfra(self, model: str, system_prompt: str, user_prompt: str, max_tokens: Optional[int] = None) -> Optional[str]:
        if not self.runinfra_key or self.runinfra_key.startswith("${"):
            return None

        import uuid
        url = f"{self.runinfra_base}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.runinfra_key}",
            "Content-Type": "application/json",
            "X-Client-Request-Id": str(uuid.uuid4())
        }
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": self.temperature,
            "max_tokens": max_tokens or self.max_tokens
        }

        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers=headers)
        try:
            with urllib.request.urlopen(req, timeout=4) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                choice = data.get("choices", [{}])[0]
                msg = choice.get("message", {})
                content = msg.get("content")
                if not content:
                    content = msg.get("reasoning")
                return content
        except Exception:
            return None

    def chat_complete(self, system_prompt: str, user_prompt: str, max_tokens: Optional[int] = None) -> Optional[str]:
        """
        Executes a prompt across the priority chain with fast failover.
        """
        for model in self.openrouter_models[:2]:
            content = self._call_openrouter(model, system_prompt, user_prompt, max_tokens)
            if content:
                return content

        cc_content = self._call_codecraft(system_prompt, user_prompt)
        if cc_content:
            return cc_content

        for model in self.runinfra_models:
            content = self._call_runinfra(model, system_prompt, user_prompt, max_tokens)
            if content:
                return content

        return None

    def parse_json_response(self, text: Optional[str]) -> Any:
        """
        Robustly extracts JSON from LLM response text even with markdown wrappers.
        """
        if not text:
            return None

        # Clean markdown codeblocks
        match = re.search(r"```(?:json)?\s*([\[\{].*?[\]\}])\s*```", text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group(1))
            except Exception:
                pass

        match_raw = re.search(r"([\[\{].*[\]\}])", text, re.DOTALL)
        if match_raw:
            try:
                return json.loads(match_raw.group(1))
            except Exception:
                pass

        try:
            return json.loads(text)
        except Exception:
            return None

    def analyze_topic(self, topic_input: str) -> Dict[str, Any]:
        """
        Analyzes the topics entered by the student at the beginning of the notebook.
        Generates core learning pillars, pitfalls, and diagnostic checklist.
        """
        topic_lower = (topic_input or "").lower()
        if any(k in topic_lower for k in ["bind", "partial", "lost this", "context", "curry"]):
            return {
                "topic_summary": "How JavaScript determines this, how binding and partial application preserve or lose execution context, and how to create partial functions with or without a fixed this.",
                "key_mental_models": [
                    "`this` is determined by the call site at runtime, not where the function was declared",
                    "`bind()` locks both `this` and initial arguments, while partial application fixes arguments only",
                    "Arrow functions permanently inherit lexical `this` from outer scope and ignore `.bind()`, `.call()`, or `.apply()`"
                ],
                "common_pitfalls": [
                    "Detaching object methods when passing them as callbacks (e.g. `setTimeout(obj.method, 100)`)",
                    "Confusing partial application (argument fixing) with method binding (context locking)",
                    "Attempting to rebind `this` on arrow functions",
                    "Unintentional strict-mode `undefined` vs non-strict global `window`/`globalThis` fallback"
                ],
                "mastery_checklist": [
                    "Predict the runtime value of `this` across standalone calls, method calls, and callbacks",
                    "Implement custom `bind()`, `partial()`, and `partialWithoutContext()` functions",
                    "Handle argument prepending, dynamic arity, and recursive currying",
                    "Preserve or strip caller context across composition pipelines and switchboards"
                ],
                "recommended_focus": "Trace the call site first, determine if context needs to be preserved or stripped, and combine pre-bound arguments with runtime arguments."
            }

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
  "common_pitfalls": ["Pitfall 1", "Pitfall 2"],
  "mastery_checklist": ["What you must master 1", "What you must master 2"],
  "recommended_focus": "Advice for tackling the 10 diagnostic test questions"
}}
"""
        response_text = self.chat_complete(system_prompt, user_prompt, max_tokens=1500)
        parsed = self.parse_json_response(response_text)
        if not parsed or not isinstance(parsed, dict) or "topic_summary" not in parsed:
            parsed = {
                "topic_summary": f"In-depth curriculum analysis for: {topic_input or 'JavaScript Mastery'}",
                "key_mental_models": [
                    f"Core Execution Mechanics of {topic_input}",
                    "State & Argument Flow Preservation",
                    "Higher-Order Abstraction & Boundary Conditions"
                ],
                "common_pitfalls": [
                    "Losing execution context or parameters across asynchronous boundaries",
                    "Shadowing variables and mutation of shared references",
                    "Failing to handle edge-case inputs and error states"
                ],
                "mastery_checklist": [
                    "Master fundamental implementation and syntax patterns",
                    "Handle timer, async queues, and lifecycle hooks correctly",
                    "Implement composition, factories, and debugging diagnostics"
                ],
                "recommended_focus": "Focus on pure transformations, context forwarding, and edge-case validation."
            }
        return parsed

    def generate_questions_for_topic(self, topic: str) -> List[Dict[str, Any]]:
        """
        Dynamically generates 10 progressive difficulty questions strictly tailored to the topic
        following the 10-tier blueprint in plan.md.
        """
        system_prompt = (
            "You are a principal software engineering instructor. "
            "Generate an interactive 10-question progressive mastery test suite tailored specifically to the given topic. "
            "Return ONLY a JSON array containing 10 question objects. No markdown preamble or conversational filler."
        )

        user_prompt = f"""
STUDENT'S ENTERED TOPIC:
{topic}

Generate exactly 10 questions following this progressive difficulty structure:
- Q1: Fundamental implementation (core mechanics of {topic})
- Q2: Metadata / state tracking on top of {topic}
- Q3: Core conceptual deep-dive & edge-case handling
- Q4: Timing / Asynchronous / Lifecycle pattern in {topic}
- Q5: Composition / Pipeline / Chaining of multiple operations
- Q6: Preserving properties, descriptors, or non-functional constraints
- Q7: Factory pattern / Configurable higher-order abstractions
- Q8: Bug hunt: Debugging subtle edge cases or anti-patterns
- Q9: Real-world integration / Concurrency / Rate-limiting / Queueing
- Q10: Diagnostic challenge: Complex multi-tier scenario with error recovery

Each question object in the JSON array MUST have these keys:
- "id": integer 1-10
- "title": concise descriptive title
- "difficulty": "Fundamental" | "Intermediate" | "Advanced" | "Expert"
- "concepts": array of strings (concepts tested)
- "description": clear markdown instructions with requirements
- "starter_code": JavaScript starter function template
- "test_suite_js": JavaScript test code using `await test('name', () => {{ assertEqual(actual, expected); }})` and `assert(condition, message)`
- "solution_code": Complete working JavaScript reference solution
- "explanation": Why the solution works and key insight
- "hints": array of 3 hint objects:
    [
      {{"tier": 1, "title": "Conceptual Nudge", "content": "..."}},
      {{"tier": 2, "title": "Approach Strategy", "content": "..."}},
      {{"tier": 3, "title": "Code Skeleton", "content": "```javascript\\n...\\n```"}}
    ]

Return ONLY the JSON array `[...]`.
"""
        response_text = self.chat_complete(system_prompt, user_prompt, max_tokens=4000)
        parsed = self.parse_json_response(response_text)

        if parsed and isinstance(parsed, list) and len(parsed) >= 1:
            # Normalize IDs and ensure all keys exist
            questions = []
            for idx, q in enumerate(parsed[:10], start=1):
                q["id"] = idx
                if "hints" not in q or len(q["hints"]) < 3:
                    q["hints"] = [
                        {"tier": 1, "title": "Conceptual Nudge", "content": f"Focus on how {q.get('title', 'this concept')} operates in {topic}."},
                        {"tier": 2, "title": "Approach Strategy", "content": "Handle input arguments, perform the core transformation, and return expected outputs."},
                        {"tier": 3, "title": "Code Skeleton", "content": f"```javascript\n{q.get('starter_code', '// write solution')}\n```"}
                    ]
                questions.append(q)
            return questions

        # If AI generation is offline or incomplete, procedurally synthesize challenges tailored to this topic
        from synthetic_engine import generate_synthetic_suite
        return generate_synthetic_suite(topic)

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
        Autonomous backend evaluation combining deterministic Node.js test runs with AI feedback.
        """
        total_tests = test_results.get("total", 0)
        passed_tests = test_results.get("passed", 0)
        failed_tests = test_results.get("failed", 0)
        all_passed = (total_tests > 0 and failed_tests == 0 and not test_results.get("error"))

        system_prompt = (
            "You are an automated grading engine. Evaluate the student's code and test results. "
            "Return ONLY valid JSON."
        )

        user_prompt = f"""
QUESTION #{question_id}: {question_title}
DESCRIPTION: {question_desc}
CONCEPTS: {', '.join(expected_concepts)}

STUDENT CODE:
```javascript
{student_code}
```

TEST RESULTS:
- Total: {total_tests}, Passed: {passed_tests}, Failed: {failed_tests}
- Details: {json.dumps(test_results.get('tests', []))}
- Error: {test_results.get('error', 'None')}

Return ONLY JSON:
{{
  "verdict": "correct" | "partially_correct" | "incorrect",
  "score": <0-100>,
  "explanation": "<2-sentence pedagogical assessment>",
  "key_insight": "<core takeaway>",
  "next_steps": "<actionable advice>"
}}
"""
        response_text = self.chat_complete(system_prompt, user_prompt, max_tokens=1000)
        res = self.parse_json_response(response_text)

        if not res or "score" not in res or not isinstance(res.get("score"), (int, float)):
            res = {}
            if all_passed:
                res["score"] = 100
                res["verdict"] = "correct"
                res["explanation"] = "All test cases and assertions passed flawlessly!"
                res["key_insight"] = f"Excellent implementation of {expected_concepts[0] if expected_concepts else question_title}."
                res["next_steps"] = "Great job! Move forward to the next challenge."
            elif passed_tests > 0:
                res["score"] = int((passed_tests / max(total_tests, 1)) * 80)
                res["verdict"] = "partially_correct"
                res["explanation"] = f"Passed {passed_tests} of {total_tests} test cases. Some edge cases failed."
                res["key_insight"] = "Check edge cases and function return values."
                res["next_steps"] = "Inspect the test failure details and consult the hints."
            else:
                res["score"] = 20
                res["verdict"] = "incorrect"
                err = test_results.get("error") or "Test assertions failed."
                res["explanation"] = f"Execution did not pass assertions: {err}"
                res["key_insight"] = "Review the core mechanics required by the problem."
                res["next_steps"] = "Read Hint 1 and Hint 2 for guided structure."

        if "verdict" not in res:
            res["verdict"] = "correct" if res["score"] >= self.passing_score else ("partially_correct" if res["score"] >= self.partial_score_min else "incorrect")

        return res
