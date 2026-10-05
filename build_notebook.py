"""
Rebuilds decorator_mastery_test.ipynb as a clean, interactive dynamic learning suite.
"""

import nbformat as nbf


def generate_interactive_notebook():
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

    header_md = """# 🚀 Interactive Dynamic Mastery Assessment Suite
### Powered by Autonomous AI Grading & Node.js Subprocess Sandbox

Welcome to the **Dynamic Assessment Suite**! 

#### 📋 How It Works:
1. **Enter Your Topic Below:** Type whatever programming topic you studied today (e.g. *JavaScript Decorators & call/apply*, *React useEffect & Lifecycle*, *Async/Await & Promises*, etc.).
2. **Click "Analyze Topic & Generate 10 Challenges":** The AI will analyze the topic and dynamically generate **10 custom progressive challenges** (Fundamentals $\\rightarrow$ Advanced $\\rightarrow$ Bug Hunt $\\rightarrow$ Expert Diagnostic) matching the blueprint in `plan.md`.
3. **Solve & Submit:** Write your solution in each question's interactive code area and click **Submit & Evaluate**.
4. **Autonomous Backend Evaluation:** All testing runs autonomously in the backend (Node.js test execution + AI pedagogical evaluation) without exposing evaluation boilerplate to you.
"""
    cells.append(nbf.v4.new_markdown_cell(header_md))

    launch_code = """# === LAUNCH INTERACTIVE MASTERY APPLICATION ===
from notebook_engine import MasteryApp

# Initialize and launch dynamic assessment harness
app = MasteryApp()
app.launch()
"""
    cells.append(nbf.v4.new_code_cell(launch_code))

    nb["cells"] = cells
    return nb


if __name__ == "__main__":
    nb = generate_interactive_notebook()
    with open("decorator_mastery_test.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb, f)
    print("[OK] Rebuilt decorator_mastery_test.ipynb cleanly.")
