"""
NotebookEngine: Interactive UI and dynamic question runner for Jupyter Notebooks.
Provides interactive widget application with zero exposed evaluation boilerplate.
"""

import json
from IPython.display import display, HTML, clear_output
import ipywidgets as widgets
from js_evaluator import JSEvaluator
from ai_evaluator import AIEvaluator
from questions import ALL_QUESTIONS


class MasteryApp:
    def __init__(self):
        self.js_evaluator = JSEvaluator()
        self.ai_evaluator = AIEvaluator()
        self.current_topic = ""
        self.topic_analysis = {}
        self.questions = []
        self.session_progress = {}

    def launch(self):
        """Renders the initial interactive topic intake cell."""
        out = widgets.Output()

        topic_text = widgets.Text(
            value="JavaScript Decorators, call/apply, method borrowing, and function forwarding",
            placeholder="e.g. JavaScript Async/Await, Promises & Event Loop",
            description="Topic:",
            layout=widgets.Layout(width="70%")
        )

        gen_button = widgets.Button(
            description="⚡ Analyze Topic & Generate 10 Challenges",
            button_style="primary",
            tooltip="Analyze entered topic and generate 10 progressive questions",
            layout=widgets.Layout(width="380px", height="40px", margin="10px 0")
        )

        def on_click(b):
            topic = topic_text.value.strip()
            if not topic:
                with out:
                    clear_output()
                    print("⚠️ Please enter a valid topic name.")
                return

            with out:
                clear_output()
                display(HTML(f"""
                <div style="padding: 12px; background: #EFF6FF; border-left: 4px solid #3B82F6; border-radius: 4px; color: #1E40AF; font-family: sans-serif;">
                    ⏳ <strong>Analyzing '{topic}'...</strong> Generating 10 progressive challenges in the background...
                </div>
                """))

            self.current_topic = topic
            self.topic_analysis = self.ai_evaluator.analyze_topic(topic)
            self.questions = self.ai_evaluator.generate_questions_for_topic(topic)
            self.session_progress = {
                q["id"]: {"score": 0, "verdict": "unattempted", "attempts": 0, "last_code": q.get("starter_code", "")}
                for q in self.questions
            }

            with out:
                clear_output()
                self._render_mastery_suite(out)

        gen_button.on_click(on_click)

        panel = widgets.VBox([
            widgets.HTML("""
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin-bottom: 12px;">
                <h2 style="color: #1E293B; margin: 0 0 6px 0;">🎯 Enter What You Learned Today</h2>
                <p style="color: #64748B; margin: 0; font-size: 14px;">
                    Enter any JavaScript or programming concept. The AI will analyze your curriculum and dynamically generate 10 tailored challenges (from Fundamentals to Expert Diagnostic).
                </p>
            </div>
            """),
            widgets.HBox([topic_text]),
            gen_button,
            out
        ], layout=widgets.Layout(padding="16px", border="1px solid #E2E8F0", border_radius="10px", background="#FFFFFF"))

        display(panel)

    def _render_mastery_suite(self, container_output):
        """Renders the topic analysis overview, dynamic 10 questions accordion, and scoreboard."""
        
        # 1. Topic Blueprint Header
        models_li = "".join([f"<li style='margin-bottom:4px;'>{m}</li>" for m in self.topic_analysis.get('key_mental_models', [])])
        pitfalls_li = "".join([f"<li style='margin-bottom:4px;'>⚠️ {p}</li>" for p in self.topic_analysis.get('common_pitfalls', [])])
        checklist_li = "".join([f"<li style='margin-bottom:4px;'>☑️ {c}</li>" for c in self.topic_analysis.get('mastery_checklist', [])])

        header_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: linear-gradient(135deg, #0F172A 0%, #1E293B 100%); color: #F8FAFC; border-radius: 10px; padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <h3 style="margin:0; color:#38BDF8;">🧠 Learning Blueprint: {self.current_topic}</h3>
                <span style="background:#0284C7; color:white; font-size:12px; font-weight:bold; padding:3px 10px; border-radius:12px;">10 Questions Ready</span>
            </div>
            <p style="color:#CBD5E1; margin:8px 0 14px 0; font-size:14px; font-style:italic;">"{self.topic_analysis.get('topic_summary')}"</p>
            
            <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px;">
                <div style="background:rgba(255,255,255,0.05); padding:10px 14px; border-radius:6px; border:1px solid rgba(255,255,255,0.1);">
                    <h5 style="margin:0 0 6px 0; color:#67E8F9; font-size:13px;">🔑 Key Mental Models</h5>
                    <ul style="margin:0; padding-left:16px; font-size:12px; color:#E2E8F0;">{models_li}</ul>
                </div>
                <div style="background:rgba(255,255,255,0.05); padding:10px 14px; border-radius:6px; border:1px solid rgba(255,255,255,0.1);">
                    <h5 style="margin:0 0 6px 0; color:#FCA5A5; font-size:13px;">🚨 Common Pitfalls</h5>
                    <ul style="margin:0; padding-left:16px; font-size:12px; color:#E2E8F0;">{pitfalls_li}</ul>
                </div>
            </div>
        </div>
        """
        display(HTML(header_html))

        # 2. Build 10 Interactive Question Accordion Tabs
        accordion_children = []
        accordion_titles = []

        for q in self.questions:
            qid = q["id"]
            title = q["title"]
            diff = q.get("difficulty", "General")
            accordion_titles.append(f"Q{qid}: {title} ({diff})")

            # Question Content Widget
            hints_html = ""
            for h in q.get("hints", []):
                hints_html += f"""
                <details style="margin: 6px 0; background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 6px; padding: 8px 12px; cursor: pointer;">
                  <summary style="font-weight: 600; color: #2563EB;">💡 Hint {h.get('tier', 1)}: {h.get('title', 'Hint')}</summary>
                  <div style="margin-top: 8px; color: #334155; font-size: 13px;">{h.get('content', '')}</div>
                </details>
                """

            q_header = widgets.HTML(f"""
            <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; margin-bottom: 10px;">
                <h4 style="margin: 0 0 6px 0; color: #1E293B;">Q{qid}: {title}</h4>
                <div style="font-size: 13px; color: #64748B; margin-bottom: 10px;">
                    <strong>Difficulty:</strong> <span style="background:#E2E8F0; padding:2px 6px; border-radius:4px;">{diff}</span> &nbsp;|&nbsp; 
                    <strong>Concepts:</strong> {', '.join(q.get('concepts', []))}
                </div>
                <div style="background: #F8FAFC; padding: 12px; border-radius: 6px; border: 1px solid #E2E8F0; font-size: 14px; color: #334155; line-height: 1.5;">
                    {q.get('description', '')}
                </div>
                <div style="margin-top: 10px;">{hints_html}</div>
            </div>
            """)

            # Code Input Area
            code_input = widgets.Textarea(
                value=q.get("starter_code", ""),
                placeholder="Write your JavaScript solution here...",
                layout=widgets.Layout(width="100%", height="220px", font_family="monospace")
            )

            eval_btn = widgets.Button(
                description=f"🚀 Submit & Evaluate Q{qid}",
                button_style="success",
                layout=widgets.Layout(width="240px", height="36px", margin="8px 0")
            )

            feedback_output = widgets.Output()

            def make_eval_handler(q_obj=q, inp=code_input, f_out=feedback_output):
                def handler(btn):
                    code = inp.value.strip()
                    qid_local = q_obj["id"]
                    self.session_progress[qid_local]["attempts"] += 1
                    self.session_progress[qid_local]["last_code"] = code

                    with f_out:
                        clear_output()
                        display(HTML("""
                        <div style="color: #2563EB; font-size: 13px; padding: 6px 0;">
                            ⚙️ Running deterministic tests in Node.js & AI grading engine...
                        </div>
                        """))

                    # Background execution
                    test_results = self.js_evaluator.evaluate(code, q_obj.get("test_suite_js", ""))
                    eval_result = self.ai_evaluator.evaluate_question(
                        question_id=qid_local,
                        question_title=q_obj["title"],
                        question_desc=q_obj.get("description", ""),
                        expected_concepts=q_obj.get("concepts", []),
                        student_code=code,
                        test_results=test_results
                    )

                    score = eval_result.get("score", 0)
                    self.session_progress[qid_local]["score"] = score
                    self.session_progress[qid_local]["verdict"] = eval_result.get("verdict", "incorrect")

                    with f_out:
                        clear_output()
                        self._render_question_feedback(eval_result, test_results, q_obj)
                return handler

            eval_btn.on_click(make_eval_handler())

            q_panel = widgets.VBox([
                q_header,
                widgets.HTML("<strong>Your JavaScript Solution:</strong>"),
                code_input,
                eval_btn,
                feedback_output
            ], layout=widgets.Layout(padding="12px", background="#FFFFFF"))

            accordion_children.append(q_panel)

        accordion = widgets.Accordion(children=accordion_children)
        for i, t in enumerate(accordion_titles):
            accordion.set_title(i, t)

        display(accordion)

        # 3. Overall Dashboard Button
        dash_out = widgets.Output()
        dash_btn = widgets.Button(
            description="📊 View Master Scoreboard & Rank",
            button_style="info",
            layout=widgets.Layout(width="300px", height="40px", margin="20px 0 10px 0")
        )

        def on_dash_click(b):
            with dash_out:
                clear_output()
                self._render_dashboard()

        dash_btn.on_click(on_dash_click)
        display(widgets.VBox([dash_btn, dash_out]))

    def _render_question_feedback(self, eval_result, test_results, question):
        verdict = eval_result.get("verdict", "incorrect")
        score = eval_result.get("score", 0)
        qid = question["id"]
        attempts = self.session_progress[qid]["attempts"]

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
                <pre style="background:#1E293B; color:#F8FAFC; padding:10px; border-radius:6px; font-size:13px; overflow-x:auto;"><code>{question.get('solution_code', '')}</code></pre>
                <p style="margin:6px 0 0 0; font-size:13px; color:#1E40AF;"><strong>Explanation:</strong> {question.get('explanation', '')}</p>
            </details>
            """

        html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; border: 1px solid #E5E7EB; border-left: 5px solid {color}; border-radius: 6px; padding: 14px; margin: 10px 0; background: #FAFDFB;">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom: 8px;">
                <strong style="color:#1F2937; font-size:15px;">Evaluation Result (Attempt #{attempts})</strong>
                <span style="background:{color}; color:white; font-weight:bold; padding:3px 10px; border-radius:12px; font-size:13px;">
                    {verdict_label} ({score}/100)
                </span>
            </div>
            <p style="margin: 6px 0; color:#374151; font-size:13px;"><strong>Assessment:</strong> {eval_result.get('explanation')}</p>
            <p style="margin: 6px 0; color:#047857; font-size:13px;"><strong>💡 Key Insight:</strong> {eval_result.get('key_insight')}</p>
            
            <details style="margin-top:8px; cursor:pointer;">
                <summary style="font-weight:600; color:#2563EB; font-size:13px;">View Test Assertions ({test_results.get('passed', 0)}/{test_results.get('total', 0)} Passed)</summary>
                <table style="width:100%; border-collapse:collapse; margin-top:6px; background:white; border:1px solid #E5E7EB; border-radius:4px; font-size:12px;">
                    {test_rows}
                </table>
            </details>
            {solution_html}
        </div>
        """
        display(HTML(html))

    def _render_dashboard(self):
        total_score = sum(self.session_progress[q["id"]]["score"] for q in self.questions)
        avg_score = round(total_score / max(len(self.questions), 1), 1)
        passed_count = sum(1 for q in self.questions if self.session_progress[q["id"]]["score"] >= 70)

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
        for q in self.questions:
            p = self.session_progress[q["id"]]
            badge_bg = "#10B981" if p["score"] >= 70 else ("#F59E0B" if p["score"] >= 40 else "#EF4444")
            table_rows += f"""
            <tr style="border-bottom: 1px solid #E2E8F0;">
                <td style="padding: 8px 12px; font-weight: 500;">Q{q['id']}: {q['title']}</td>
                <td style="padding: 8px 12px;">{q.get('difficulty', 'General')}</td>
                <td style="padding: 8px 12px;">{p['attempts']}</td>
                <td style="padding: 8px 12px;">
                    <span style="background:{badge_bg}; color:white; padding:2px 8px; border-radius:10px; font-weight:bold; font-size:12px;">
                        {p['score']}/100
                    </span>
                </td>
            </tr>
            """

        summary_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: white; border: 1px solid #E2E8F0; border-radius: 12px; padding: 20px; margin: 10px 0; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px;">
                <h3 style="margin:0; color:#0F172A;">📊 Overall Assessment Scoreboard</h3>
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
                    <div style="font-size:22px; font-weight:bold; color:#10B981;">{passed_count} / {len(self.questions)}</div>
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
