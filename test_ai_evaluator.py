from ai_evaluator import AIEvaluator
from js_evaluator import JSEvaluator
from questions import Q1

ai = AIEvaluator()
js = JSEvaluator()

print("--- Testing Topic Analysis ---")
topic_res = ai.analyze_topic("JavaScript Decorators, call/apply, method borrowing, lost this context")
print("Topic Summary:", topic_res.get("topic_summary"))
print("Mental Models:", topic_res.get("key_mental_models"))
print("Common Pitfalls:", topic_res.get("common_pitfalls"))

print("\n--- Testing Question Evaluation ---")
test_res = js.evaluate(Q1["solution_code"], Q1["test_suite_js"])
eval_res = ai.evaluate_question(
    question_id=Q1["id"],
    question_title=Q1["title"],
    question_desc=Q1["description"],
    expected_concepts=Q1["concepts"],
    student_code=Q1["solution_code"],
    test_results=test_res
)
print("Score:", eval_res.get("score"))
print("Verdict:", eval_res.get("verdict"))
print("Explanation:", eval_res.get("explanation", "").encode("ascii", "replace").decode("ascii"))
print("Key Insight:", eval_res.get("key_insight", "").encode("ascii", "replace").decode("ascii"))

