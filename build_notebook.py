"""
Script to build decorator_mastery_test.ipynb with full interactive UI,
topic analyzer, 10 progressive questions, progressive hints, AI evaluation runners,
and master report dashboard.
"""

import json
import nbformat as nbf
from questions import ALL_QUESTIONS


def generate_notebook():
    nb = nbf.v4.new_notebook()
    nb.metadata["kernelspec"] = {
        "display_name": "Python 3",
        "language": "python",
        "name": "python3"
    }
    nb.metadata["language_info"] = {
        "name": "python",
        "version": "3.14.0"
    }

    cells = []

    # 1. Header Cell
    header_md = """# 🚀 JavaScript Decorators, `call`/`apply` & Function Forwarding
### Interactive Mastery Test Suite with Real-time AI Evaluation

Welcome to the **Interactive JavaScript Diagnostic Test Suite**! This notebook evaluates deep conceptual mastery of:
- Execution contexts, lexical vs dynamic `this`, and explicit binding with `.call()` and `.apply()`
- Function wrapping, transparent proxying, and closures
- Debouncing, throttling, concurrency queues, and async retry pipelines
- Preserving function descriptors, metadata, and chained decorator mechanics

---

### How It Works:
1. **Initialize & Set Your Topic:** In Cell 1, enter what you studied today. The AI will analyze your focus and provide a curriculum diagnosis.
2. **Solve the 10 Progressive Challenges:** Write your JavaScript code in each question's designated answer cell.
3. **Run AI Evaluation:** Execute the evaluation cell under each question to run deterministic Node.js test suites + AI pedagogical analysis.
4. **Use Progressive Hints:** Each challenge has 3 tiers of collapsible hints.
"""
    cells.append(nbf.v4.new_markdown_cell(header_md))

    # 2. Setup Code Cell
    setup_code = """# === CELL 1: INITIALIZATION & ENVIRONMENT SETUP ===
import os
import json
from IPython.display import display, HTML
import ipywidgets as widgets
from js_evaluator import JSEvaluator
from ai_evaluator import AIEvaluator
from questions import ALL_QUESTIONS, get_question

# Initialize Evaluation Engines
js_evaluator = JSEvaluator()
ai_evaluator = AIEvaluator()

# Session State
SESSION_PROGRESS = {q["id"]: {"score": 0, "verdict": "unattempted", "attempts": 0} for q in ALL_QUESTIONS}

def render_html_feedback(eval_result, test_results, question):
    verdict = eval_result.get("verdict", "incorrect")
    score = eval_result.get("score", 0)
    
    badge_colors = {
        "correct": "#10B981",
        "partially_correct": "#F59E0B",
        "incorrect": "#EF4444"
    }
    color = badge_colors.get(verdict, "#6B7280")
    verdict_label = verdict.replace("_", " ").upper()
    
    test_rows = ""
    for t in test_results.get("tests", []):
        status_icon = "✅" if t.get("passed") else "❌"
        err_msg = f"<br/><span style='color:#EF4444; font-size:12px;'>Error: {t.get('error')}</span>" if t.get('error') else ""
        test_rows += f"<tr><td style='padding:6px 12px;'>{status_icon} <strong>{t.get('name')}</strong>{err_msg}</td></tr>"

    html = f\"\"\"
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; border: 1px solid #E5E7EB; border-left: 6px solid {color}; border-radius: 8px; padding: 18px; margin: 15px 0; background: #FAFDFB;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 12px;">
            <h3 style="margin:0; color:#1F2937;">{question['title']} — Evaluation Result</h3>
            <span style="background:{color}; color:white; font-weight:bold; padding:4px 12px; border-radius:16px; font-size:14px;">
                {verdict_label} ({score}/100)
            </span>
        </div>
        <p style="margin: 8px 0; color:#374151; font-size:14px;"><strong>Feedback:</strong> {eval_result.get('explanation')}</p>
        <p style="margin: 8px 0; color:#047857; font-size:14px;"><strong>💡 Key Insight:</strong> {eval_result.get('key_insight')}</p>
        <p style="margin: 8px 0; color:#4B5563; font-size:14px;"><strong>🎯 Next Steps:</strong> {eval_result.get('next_steps')}</p>
        
        <details style="margin-top:12px; cursor:pointer;">
            <summary style="font-weight:600; color:#2563EB;">View Deterministic Unit Test Details ({test_results.get('passed', 0)}/{test_results.get('total', 0)} Passed)</summary>
            <table style="width:100%; border-collapse:collapse; margin-top:8px; background:white; border:1px solid #E5E7EB; border-radius:4px;">
                {test_rows}
            </table>
        </details>
    </div>
    \"\"\"
    display(HTML(html))

print("✅ Initialization complete! Test runner & AI Evaluator ready.")
"""
    cells.append(nbf.v4.new_code_cell(setup_code))

    # 3. Topic Input & Analysis Cell (Markdown + Code)
    topic_md = """---
## 🎯 Step 1: Set Your Learning Topic
Tell the AI what topics or subtopics you learned today (for example: *`JavaScript Decorators, call/apply, method borrowing, and lost this context`*). The AI will analyze the topic and set up your study guide and diagnostic focus.
"""
    cells.append(nbf.v4.new_markdown_cell(topic_md))

    topic_code = """# === CELL 2: TOPIC ENTRY & AI CURRICULUM DIAGNOSIS ===
# Enter the topics you learned today below:
LEARNED_TOPICS = "JavaScript Decorators, call/apply, function forwarding, and method borrowing"

print(f"🔍 Analyzing topic: '{LEARNED_TOPICS}' via AI Router...")
topic_analysis = ai_evaluator.analyze_topic(LEARNED_TOPICS)

# Render Curriculum Breakdown
models_li = "".join([f"<li style='margin-bottom:4px;'>{m}</li>" for m in topic_analysis.get('key_mental_models', [])])
pitfalls_li = "".join([f"<li style='margin-bottom:4px;'>⚠️ {p}</li>" for p in topic_analysis.get('common_pitfalls', [])])
checklist_li = "".join([f"<li style='margin-bottom:4px;'>☑️ {c}</li>" for c in topic_analysis.get('mastery_checklist', [])])

topic_html = f\"\"\"
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #1E293B 0%, #0F172A 100%); color: #F8FAFC; border-radius: 12px; padding: 24px; margin: 15px 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
    <div style="display:flex; justify-content:space-between; align-items:center;">
        <h2 style="margin:0; color:#38BDF8; font-size:20px;">🧠 Topic Diagnostic & Learning Blueprint</h2>
        <span style="background:#0284C7; color:white; font-size:12px; font-weight:bold; padding:3px 10px; border-radius:12px;">Active Plan</span>
    </div>
    <p style="color:#CBD5E1; margin:10px 0 18px 0; font-size:15px; font-style:italic;">"{topic_analysis.get('topic_summary')}"</p>
    
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; margin-bottom:16px;">
        <div style="background:rgba(255,255,255,0.05); padding:14px; border-radius:8px; border:1px solid rgba(255,255,255,0.1);">
            <h4 style="margin:0 0 8px 0; color:#67E8F9; font-size:14px;">🔑 Core Mental Models</h4>
            <ul style="margin:0; padding-left:18px; font-size:13px; color:#E2E8F0;">
                {models_li}
            </ul>
        </div>
        <div style="background:rgba(255,255,255,0.05); padding:14px; border-radius:8px; border:1px solid rgba(255,255,255,0.1);">
            <h4 style="margin:0 0 8px 0; color:#FCA5A5; font-size:14px;">🚨 Common Pitfalls to Avoid</h4>
            <ul style="margin:0; padding-left:18px; font-size:13px; color:#E2E8F0;">
                {pitfalls_li}
            </ul>
        </div>
    </div>
    
    <div style="background:rgba(56, 189, 248, 0.1); padding:14px; border-radius:8px; border:1px solid rgba(56, 189, 248, 0.2);">
        <h4 style="margin:0 0 8px 0; color:#38BDF8; font-size:14px;">📋 Test Suite Mastery Checklist</h4>
        <ul style="margin:0; padding-left:18px; font-size:13px; color:#E2E8F0;">
            {checklist_li}
        </ul>
        <p style="margin:10px 0 0 0; font-size:13px; color:#94A3B8;"><strong>Mentor Advice:</strong> {topic_analysis.get('recommended_focus')}</p>
    </div>
</div>
\"\"\"
display(HTML(topic_html))
"""
    cells.append(nbf.v4.new_code_cell(topic_code))

    # 4. Generate Question Cells for Q1 through Q10
    for q in ALL_QUESTIONS:
        qid = q["id"]
        title = q["title"]
        diff = q["difficulty"]
        concepts_str = " • ".join(q["concepts"])

        # Hints HTML details
        hints_html = ""
        for h in q["hints"]:
            hints_html += f"""
<details style="margin: 6px 0; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 8px 12px; cursor: pointer;">
  <summary style="font-weight: 600; color: #2563EB;">💡 Hint {h['tier']}: {h['title']}</summary>
  <div style="margin-top: 8px; color: #334155; font-size: 14px;">
{h['content']}
  </div>
</details>"""

        q_md = f"""---
## Question {qid}: {title}
**Difficulty:** `{diff}` | **Core Concepts:** `{concepts_str}`

{q['description']}

### 🔍 Progressive Hints
{hints_html}
"""
        cells.append(nbf.v4.new_markdown_cell(q_md))

        # Code Answer Cell
        student_cell_code = f"""# === WRITE YOUR SOLUTION FOR QUESTION {qid} BELOW ===
# %%javascript or standard JS string:
q{qid}_student_solution = \"\"\"{q['starter_code']}\"\"\"
"""
        cells.append(nbf.v4.new_code_cell(student_cell_code))

        # AI Evaluation Runner Cell
        eval_runner_code = f"""# === RUN EVALUATION FOR QUESTION {qid} ===
q = get_question({qid})
SESSION_PROGRESS[{qid}]["attempts"] += 1

# Execute deterministic test suite in Node.js
test_results = js_evaluator.evaluate(q{qid}_student_solution, q["test_suite_js"])

# Run AI evaluation & feedback
ai_result = ai_evaluator.evaluate_question(
    question_id={qid},
    question_title=q["title"],
    question_desc=q["description"],
    expected_concepts=q["concepts"],
    student_code=q{qid}_student_solution,
    test_results=test_results
)

SESSION_PROGRESS[{qid}]["score"] = ai_result.get("score", 0)
SESSION_PROGRESS[{qid}]["verdict"] = ai_result.get("verdict", "incorrect")

render_html_feedback(ai_result, test_results, q)

# Solution Reveal Trigger
if SESSION_PROGRESS[{qid}]["attempts"] >= 3 or SESSION_PROGRESS[{qid}]["score"] >= 70:
    display(HTML(f\"\"\"
    <details style="margin-top:10px; background:#EFF6FF; border:1px solid #BFDBFE; border-radius:6px; padding:10px;">
        <summary style="font-weight:bold; color:#1D4ED8; cursor:pointer;">🔓 Reveal Reference Solution</summary>
        <pre style="background:#1E293B; color:#F8FAFC; padding:12px; border-radius:6px; overflow-x:auto;"><code>{q['solution_code']}</code></pre>
        <p style="margin:6px 0 0 0; font-size:13px; color:#1E40AF;"><strong>Explanation:</strong> {q['explanation']}</p>
    </details>
    \"\"\"))
"""
        cells.append(nbf.v4.new_code_cell(eval_runner_code))

    # 5. Final Master Scoreboard & Summary
    scoreboard_md = """---
## 🏆 Overall Mastery Scoreboard & Assessment Summary
Run the cell below to calculate your overall score across all 10 questions and view your JavaScript Decorator Mastery level.
"""
    cells.append(nbf.v4.new_markdown_cell(scoreboard_md))

    scoreboard_code = """# === CELL: COMPREHENSIVE MASTERY REPORT ===
total_score = sum(SESSION_PROGRESS[q["id"]]["score"] for q in ALL_QUESTIONS)
avg_score = round(total_score / len(ALL_QUESTIONS), 1)
passed_count = sum(1 for q in ALL_QUESTIONS if SESSION_PROGRESS[q["id"]]["score"] >= 70)

if avg_score >= 85:
    rank = "🌟 JavaScript Decorator Grandmaster"
    rank_color = "#10B981"
elif avg_score >= 70:
    rank = "🚀 Advanced Functional Engineer"
    rank_color = "#0284C7"
elif avg_score >= 50:
    rank = "⚡ Intermediate Practitioner"
    rank_color = "#F59E0B"
else:
    rank = "🌱 Apprentice in Training"
    rank_color = "#EF4444"

table_rows = ""
for q in ALL_QUESTIONS:
    p = SESSION_PROGRESS[q["id"]]
    badge_bg = "#10B981" if p["score"] >= 70 else ("#F59E0B" if p["score"] >= 40 else "#EF4444")
    table_rows += f\"\"\"
    <tr style="border-bottom: 1px solid #E2E8F0;">
        <td style="padding: 8px 12px; font-weight: 500;">Q{q['id']}: {q['title']}</td>
        <td style="padding: 8px 12px;">{q['difficulty']}</td>
        <td style="padding: 8px 12px;">{p['attempts']}</td>
        <td style="padding: 8px 12px;">
            <span style="background:{badge_bg}; color:white; padding:2px 8px; border-radius:10px; font-weight:bold; font-size:12px;">
                {p['score']}/100
            </span>
        </td>
    </tr>
    \"\"\"

summary_html = f\"\"\"
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 24px; margin: 15px 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:16px;">
        <h2 style="margin:0; color:#0F172A;">📊 Overall Assessment Report</h2>
        <span style="background:{rank_color}; color:white; font-size:14px; font-weight:bold; padding:5px 14px; border-radius:20px;">
            {rank}
        </span>
    </div>
    
    <div style="display:flex; gap:20px; margin-bottom:20px;">
        <div style="flex:1; background:#F8FAFC; padding:14px; border-radius:8px; text-align:center; border:1px solid #E2E8F0;">
            <div style="font-size:24px; font-weight:bold; color:#0F172A;">{avg_score} / 100</div>
            <div style="font-size:12px; color:#64748B;">Average Score</div>
        </div>
        <div style="flex:1; background:#F8FAFC; padding:14px; border-radius:8px; text-align:center; border:1px solid #E2E8F0;">
            <div style="font-size:24px; font-weight:bold; color:#10B981;">{passed_count} / {len(ALL_QUESTIONS)}</div>
            <div style="font-size:12px; color:#64748B;">Questions Mastered</div>
        </div>
    </div>
    
    <table style="width:100%; border-collapse:collapse; font-size:14px; text-align:left;">
        <thead>
            <tr style="background:#F1F5F9; border-bottom: 2px solid #CBD5E1;">
                <th style="padding: 8px 12px;">Question</th>
                <th style="padding: 8px 12px;">Difficulty</th>
                <th style="padding: 8px 12px;">Attempts</th>
                <th style="padding: 8px 12px;">Final Score</th>
            </tr>
        </thead>
        <tbody>
            {table_rows}
        </tbody>
    </table>
</div>
\"\"\"
display(HTML(summary_html))
"""
    cells.append(nbf.v4.new_code_cell(scoreboard_code))

    nb["cells"] = cells
    return nb


if __name__ == "__main__":
    nb = generate_notebook()
    with open("decorator_mastery_test.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print("[OK] Successfully generated decorator_mastery_test.ipynb!")
