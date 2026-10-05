from js_evaluator import JSEvaluator
from questions import ALL_QUESTIONS

evaluator = JSEvaluator()
all_passed = True

for q in ALL_QUESTIONS:
    qid = q["id"]
    title = q["title"]
    print(f"Testing Q{qid}: {title}...")
    res = evaluator.evaluate(q["solution_code"], q["test_suite_js"])
    if res.get("failed", 0) > 0 or res.get("error"):
        print(f"  [FAIL] Q{qid}:", res)
        all_passed = False
    else:
        print(f"  [PASS] Q{qid} ({res.get('passed')}/{res.get('total')} tests passed)")

print("\nResult:", "ALL 10 PASSED!" if all_passed else "SOME FAILED")

