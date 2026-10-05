"""
NotebookEngine: Dynamic notebook cell generator and background evaluation engine.
Dynamically populates Jupyter Notebook cells with 10 topic-tailored questions,
answer cells, and one-line background evaluation runners.
"""

import json
import os
from typing import Any, Dict, Optional
from IPython.display import display, HTML, Javascript
import nbformat as nbf
from js_evaluator import JSEvaluator
from ai_evaluator import AIEvaluator
from questions import ALL_QUESTIONS

SUITE_STATE_FILE = "current_suite.json"
PROGRESS_STATE_FILE = "session_progress.json"

js_evaluator = JSEvaluator()
ai_evaluator = AIEvaluator()


def _save_suite(questions: list, topic_analysis: dict, topic: str):
    data = {
        "topic": topic,
        "topic_analysis": topic_analysis,
        "questions": questions
    }
    with open(SUITE_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    # Initialize progress
    progress = {
        str(q["id"]): {"score": 0, "verdict": "unattempted", "attempts": 0}
        for q in questions
    }
    with open(PROGRESS_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


def _load_suite() -> Dict[str, Any]:
    if os.path.exists(SUITE_STATE_FILE):
        try:
            with open(SUITE_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"topic": "JavaScript Decorators", "questions": ALL_QUESTIONS, "topic_analysis": {}}


def _load_progress() -> Dict[str, Any]:
    if os.path.exists(PROGRESS_STATE_FILE):
        try:
            with open(PROGRESS_STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {}


def _save_progress(progress: dict):
    with open(PROGRESS_STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(progress, f, indent=2)


def set_topic(topic: str):
    """
    Sets the active topic, analyzes it, loads the 10 tailored challenges into memory,
    and updates session state without file save conflicts.
    """
    display(HTML(f"""
    <div style="font-family: sans-serif; padding: 14px; background: #EFF6FF; border-left: 4px solid #3B82F6; border-radius: 6px; color: #1E40AF; margin-bottom: 12px;">
        ⏳ <strong>Configuring topic: '{topic}'...</strong> Loading 10 tailored challenges into session...
    </div>
    """))

    topic_analysis = ai_evaluator.analyze_topic(topic)
    questions = ai_evaluator.generate_questions_for_topic(topic)
    _save_suite(questions, topic_analysis, topic)

    # Render Topic Analysis Blueprint in the output
    models_li = "".join([f"<li style='margin-bottom:4px;'>{m}</li>" for m in topic_analysis.get('key_mental_models', [])])
    pitfalls_li = "".join([f"<li style='margin-bottom:4px;'>⚠️ {p}</li>" for p in topic_analysis.get('common_pitfalls', [])])
    checklist_li = "".join([f"<li style='margin-bottom:4px;'>☑️ {c}</li>" for c in topic_analysis.get('mastery_checklist', [])])

    blueprint_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #F8FAFC; border-radius: 10px; padding: 20px; margin: 12px 0 20px 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h3 style="margin:0; color:#38BDF8;">🧠 Topic Blueprint: {topic}</h3>
            <span style="background:#0284C7; color:white; font-size:12px; font-weight:bold; padding:3px 10px; border-radius:12px;">10 Questions Ready</span>
        </div>
        <p style="color:#CBD5E1; margin:8px 0 14px 0; font-size:14px; font-style:italic;">"{topic_analysis.get('topic_summary')}"</p>
        
        <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; margin-bottom: 12px;">
            <div style="background:rgba(255,255,255,0.05); padding:10px 14px; border-radius:6px; border:1px solid rgba(255,255,255,0.1);">
                <h5 style="margin:0 0 6px 0; color:#67E8F9; font-size:13px;">🔑 Key Mental Models</h5>
                <ul style="margin:0; padding-left:16px; font-size:12px; color:#E2E8F0;">{models_li}</ul>
            </div>
            <div style="background:rgba(255,255,255,0.05); padding:10px 14px; border-radius:6px; border:1px solid rgba(255,255,255,0.1);">
                <h5 style="margin:0 0 6px 0; color:#FCA5A5; font-size:13px;">🚨 Common Pitfalls</h5>
                <ul style="margin:0; padding-left:16px; font-size:12px; color:#E2E8F0;">{pitfalls_li}</ul>
            </div>
        </div>
        <div style="background:rgba(56, 189, 248, 0.1); padding:10px 14px; border-radius:6px; border:1px solid rgba(56, 189, 248, 0.2);">
            <h5 style="margin:0 0 4px 0; color:#38BDF8; font-size:13px;">📋 Mastery Checklist</h5>
            <ul style="margin:0; padding-left:16px; font-size:12px; color:#E2E8F0;">{checklist_li}</ul>
        </div>
    </div>
    """
    display(HTML(blueprint_html))

    display(HTML(f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; padding: 14px 18px; background: #ECFDF5; border: 1px solid #A7F3D0; border-left: 5px solid #10B981; border-radius: 8px; color: #065F46; margin: 15px 0;">
        <h4 style="margin:0 0 6px 0; color:#047857;">✅ Assessment Suite Active for: {topic}</h4>
        <p style="margin:0; font-size:14px;">
            10 questions loaded! Run the Question 1 cell below (or <code>show(1)</code>) to view instructions and begin solving.
        </p>
    </div>
    """))


def generate_suite(topic: str, *args, **kwargs):
    """Alias for set_topic for seamless backward compatibility."""
    return set_topic(topic)


def show(question_id: int):
    """
    Renders the question prompt, difficulty, core concepts, problem statement,
    and progressive collapsible hint accordions in rich HTML.
    """
    suite_data = _load_suite()
    questions = suite_data.get("questions", ALL_QUESTIONS)
    
    q_obj = None
    for q in questions:
        if q["id"] == question_id:
            q_obj = q
            break

    if not q_obj:
        print(f"❌ Question {question_id} not found in current suite.")
        return

    diff = q_obj.get("difficulty", "Fundamental")
    diff_colors = {
        "Fundamental": "#10B981",
        "Intermediate": "#3B82F6",
        "Advanced": "#F59E0B",
        "Expert": "#EF4444"
    }
    diff_color = diff_colors.get(diff, "#6B7280")
    
    concepts = q_obj.get("concepts", [])
    concept_pills = "".join([
        f"<span style='background:rgba(59,130,246,0.1); color:#2563EB; font-size:11px; font-weight:600; padding:2px 8px; border-radius:12px; margin-right:6px;'>{c}</span>"
        for c in concepts
    ])

    hints_html = ""
    for h in q_obj.get("hints", []):
        hints_html += f"""
        <details style="margin: 6px 0; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 8px 12px; cursor: pointer;">
          <summary style="font-weight: 600; color: #2563EB; font-size: 13px;">💡 Hint {h.get('tier', 1)}: {h.get('title', 'Hint')}</summary>
          <div style="margin-top: 8px; color: #334155; font-size: 13px; line-height: 1.5;">
            {h.get('content', '').replace(chr(10), '<br/>')}
          </div>
        </details>
        """

    # Format description markdown as readable HTML
    desc = q_obj.get("description", "").strip()
    # Simple markdown cleaner for display
    desc_html = desc.replace("\n", "<br/>")

    html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: white; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px; margin: 12px 0; box-shadow: 0 2px 4px rgba(0,0,0,0.04);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 10px; border-bottom: 1px solid #F1F5F9; padding-bottom: 10px;">
            <div>
                <span style="font-size:12px; font-weight:bold; color:#64748B; text-transform:uppercase; letter-spacing:0.5px;">Question {question_id} of {len(questions)}</span>
                <h3 style="margin:4px 0 0 0; color:#0F172A; font-size:18px;">{q_obj.get('title')}</h3>
            </div>
            <span style="background:{diff_color}; color:white; font-size:12px; font-weight:bold; padding:4px 12px; border-radius:12px;">
                {diff}
            </span>
        </div>
        
        <div style="margin-bottom: 14px;">
            {concept_pills}
        </div>
        
        <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:6px; padding:14px; color:#1E293B; font-size:14px; line-height:1.6; margin-bottom:14px;">
            {desc_html}
        </div>
        
        <div style="margin-bottom: 8px;">
            <strong style="color:#0F172A; font-size:13px;">🔍 Progressive Hints (Click to expand if needed):</strong>
            {hints_html}
        </div>
    </div>
    """
    display(HTML(html))


# Aliases
show_question = show
q = show


def evaluate(question_id: int, student_code: str):
    """
    Evaluates the student's solution for a given question autonomously in the background.
    """
    suite_data = _load_suite()
    questions = suite_data.get("questions", ALL_QUESTIONS)
    
    # Find question object
    q_obj = None
    for q in questions:
        if q["id"] == question_id:
            q_obj = q
            break

    if not q_obj:
        print(f"❌ Question {question_id} not found in current suite.")
        return

    progress = _load_progress()
    qid_key = str(question_id)
    if qid_key not in progress:
        progress[qid_key] = {"score": 0, "verdict": "unattempted", "attempts": 0}
    progress[qid_key]["attempts"] += 1
    attempts = progress[qid_key]["attempts"]

    # Background execution in Node.js
    test_results = js_evaluator.evaluate(student_code, q_obj.get("test_suite_js", ""))

    # Background AI grading
    eval_result = ai_evaluator.evaluate_question(
        question_id=question_id,
        question_title=q_obj.get("title", f"Question {question_id}"),
        question_desc=q_obj.get("description", ""),
        expected_concepts=q_obj.get("concepts", []),
        student_code=student_code,
        test_results=test_results
    )

    score = eval_result.get("score", 0)
    verdict = eval_result.get("verdict", "incorrect")
    progress[qid_key]["score"] = score
    progress[qid_key]["verdict"] = verdict
    _save_progress(progress)

    # Render clean visual feedback
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
        test_rows += f"<tr><td style='padding:6px 10px; border-bottom:1px solid #E5E7EB;'>{status_icon} <strong>{t.get('name')}</strong>{err_msg}</td></tr>"

    solution_html = ""
    if score >= 70 or attempts >= 3:
        solution_html = f"""
        <details style="margin-top:10px; background:#EFF6FF; border:1px solid #BFDBFE; border-radius:6px; padding:10px;">
            <summary style="font-weight:bold; color:#1D4ED8; cursor:pointer;">🔓 Reveal Reference Solution</summary>
            <pre style="background:#1E293B; color:#F8FAFC; padding:10px; border-radius:6px; font-size:13px; overflow-x:auto;"><code>{q_obj.get('solution_code', '')}</code></pre>
            <p style="margin:6px 0 0 0; font-size:13px; color:#1E40AF;"><strong>Explanation:</strong> {q_obj.get('explanation', '')}</p>
        </details>
        """

    feedback_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; border: 1px solid #E5E7EB; border-left: 5px solid {color}; border-radius: 6px; padding: 14px; margin: 10px 0; background: #FAFDFB;">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
            <strong style="color:#1F2937; font-size:15px;">Q{question_id}: {q_obj.get('title')} (Attempt #{attempts})</strong>
            <span style="background:{color}; color:white; font-weight:bold; padding:3px 10px; border-radius:12px; font-size:13px;">
                {verdict_label} ({score}/100)
            </span>
        </div>
        <p style="margin: 6px 0; color:#374151; font-size:13px;"><strong>Feedback:</strong> {eval_result.get('explanation')}</p>
        <p style="margin: 6px 0; color:#047857; font-size:13px;"><strong>💡 Key Insight:</strong> {eval_result.get('key_insight')}</p>
        <p style="margin: 6px 0; color:#4B5563; font-size:13px;"><strong>🎯 Next Steps:</strong> {eval_result.get('next_steps')}</p>
        
        <details style="margin-top:8px; cursor:pointer;">
            <summary style="font-weight:600; color:#2563EB; font-size:13px;">View Test Assertions ({test_results.get('passed', 0)}/{test_results.get('total', 0)} Passed)</summary>
            <table style="width:100%; border-collapse:collapse; margin-top:6px; background:white; border:1px solid #E5E7EB; border-radius:4px; font-size:12px;">
                {test_rows}
            </table>
        </details>
        {solution_html}
    </div>
    """
    display(HTML(feedback_html))


def show_scoreboard():
    """
    Renders the overall scoreboard across all 10 questions.
    """
    suite_data = _load_suite()
    questions = suite_data.get("questions", ALL_QUESTIONS)
    progress = _load_progress()

    total_score = sum(progress.get(str(q["id"]), {}).get("score", 0) for q in questions)
    avg_score = round(total_score / max(len(questions), 1), 1)
    passed_count = sum(1 for q in questions if progress.get(str(q["id"]), {}).get("score", 0) >= 70)

    if avg_score >= 85:
        rank = "🌟 Master Practitioner"
        rank_color = "#10B981"
    elif avg_score >= 70:
        rank = "🚀 Advanced Engineer"
        rank_color = "#0284C7"
    elif avg_score >= 50:
        rank = "⚡ Intermediate Learner"
        rank_color = "#F59E0B"
    else:
        rank = "🌱 Apprentice"
        rank_color = "#EF4444"

    table_rows = ""
    for q in questions:
        qid_key = str(q["id"])
        p = progress.get(qid_key, {"score": 0, "attempts": 0})
        score = p.get("score", 0)
        attempts = p.get("attempts", 0)
        badge_bg = "#10B981" if score >= 70 else ("#F59E0B" if score >= 40 else "#EF4444")
        table_rows += f"""
        <tr style="border-bottom: 1px solid #E2E8F0;">
            <td style="padding: 8px 12px; font-weight: 500;">Q{q['id']}: {q.get('title')}</td>
            <td style="padding: 8px 12px;">{q.get('difficulty', 'General')}</td>
            <td style="padding: 8px 12px;">{attempts}</td>
            <td style="padding: 8px 12px;">
                <span style="background:{badge_bg}; color:white; padding:2px 8px; border-radius:10px; font-weight:bold; font-size:12px;">
                    {score}/100
                </span>
            </td>
        </tr>
        """

    summary_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
            <h3 style="margin:0; color:#0F172A;">📊 Overall Assessment Scoreboard: {suite_data.get('topic', 'JavaScript')}</h3>
            <span style="background:{rank_color}; color:white; font-size:13px; font-weight:bold; padding:4px 12px; border-radius:20px;">
                {rank}
            </span>
        </div>
        
        <div style="display:flex; gap:16px; margin-bottom:16px;">
            <div style="flex:1; background:#F8FAFC; padding:12px; border-radius:8px; text-align:center; border:1px solid #E2E8F0;">
                <div style="font-size:22px; font-weight:bold; color:#0F172A;">{avg_score} / 100</div>
                <div style="font-size:12px; color:#64748B;">Average Score</div>
            </div>
            <div style="flex:1; background:#F8FAFC; padding:12px; border-radius:8px; text-align:center; border:1px solid #E2E8F0;">
                <div style="font-size:22px; font-weight:bold; color:#10B981;">{passed_count} / {len(questions)}</div>
                <div style="font-size:12px; color:#64748B;">Questions Mastered</div>
            </div>
        </div>
        
        <table style="width:100%; border-collapse:collapse; font-size:13px; text-align:left;">
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
    """
    display(HTML(summary_html))
