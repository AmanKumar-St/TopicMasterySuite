"""
Rebuilds decorator_mastery_test.ipynb cleanly without file conflict locks.
"""

import nbformat as nbf
from topic_curriculum import BINDING_AND_PARTIALS_QUESTIONS


def build_notebook(topic: str = "function binding , lost this , partial function , Going partial without context", filename: str = "decorator_mastery_test.ipynb"):
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

    # Title Markdown Cell
    cells.append(nbf.v4.new_markdown_cell(f"""# 🚀 Dynamic JavaScript Mastery Suite
### Topic: {topic}
Run the setup cell below, then solve each question and run its `evaluate(...)` cell for instant feedback.
"""))

    # Setup cell
    topic_cell = f"""# === TOPIC SETUP CELL ===
# Change the topic anytime and re-run this cell to switch topics without save conflicts!
from notebook_engine import set_topic, show, evaluate, show_scoreboard

TOPIC = \"\"\"{topic}\"\"\"

set_topic(TOPIC)
"""
    cells.append(nbf.v4.new_code_cell(topic_cell))

    for q in BINDING_AND_PARTIALS_QUESTIONS:
        qid = q["id"]
        title = q["title"]
        starter = q.get("starter_code", "// Write your JavaScript code here")

        # Question Display Cell
        view_cell = f"""# === QUESTION {qid}: {title} ===
show({qid})
"""
        cells.append(nbf.v4.new_code_cell(view_cell))

        # Answer Solution Cell
        ans_cell = f"""# === QUESTION {qid} ANSWER CELL ===
# Write your JavaScript solution below:
q{qid}_solution = \"\"\"{starter}\"\"\"
"""
        cells.append(nbf.v4.new_code_cell(ans_cell))

        # Evaluation Cell
        eval_cell = f"""# === QUESTION {qid} EVALUATION CELL ===
# Run this cell to check your solution for Question {qid}:
evaluate({qid}, q{qid}_solution)
"""
        cells.append(nbf.v4.new_code_cell(eval_cell))

    # Scoreboard
    cells.append(nbf.v4.new_markdown_cell("""---
## 🏆 Overall Mastery Scoreboard
Run the cell below to see your aggregate performance across all 10 challenges.
"""))
    cells.append(nbf.v4.new_code_cell("""# === FINAL MASTERY SCOREBOARD CELL ===
show_scoreboard()
"""))

    nb["cells"] = cells

    with open(filename, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    print(f"[OK] Rebuilt {filename} with {len(cells)} cells successfully.")


if __name__ == "__main__":
    build_notebook()
