# JavaScript Decorators & call/apply Mastery Test Suite

An interactive Jupyter Notebook test suite with automated Node.js execution and AI-powered pedagogical evaluation.

---

## 🌟 Features

- **Interactive Topic Intake & Curriculum Diagnostic (Cell 1):** Enter what topics you learned today to receive an AI-generated learning blueprint, core mental models, and common pitfalls to avoid.
- **10 Progressive Mastery Challenges:**
  1. **Q1:** Transparent Caching with Context (`func.call`, `this` forwarding)
  2. **Q2:** Spy Decorator with Call History (`func.apply`, function metadata)
  3. **Q3:** Method Borrowing Deep-Dive (`[].slice.call`, array-like objects)
  4. **Q4:** Debounce with Context Preservation (`setTimeout`, trailing capture)
  5. **Q5:** Decorator Composition Engine (onion-skin reduction flow)
  6. **Q6:** Preserving Function Properties & Metadata (`Object.getOwnPropertyDescriptors`)
  7. **Q7:** Curried Retry Decorator Factory (async retry loop + backoff)
  8. **Q8:** Lexical Scope & Arguments Bug Hunt (arrow function vs `function` keyword)
  9. **Q9:** Async Concurrency Limiter Decorator (Promise queues + pacing)
  10. **Q10:** Chained Decorator Diagnostic & Context Recovery
- **Deterministic Node.js Sandbox:** Every solution is executed in Node.js against real unit test suites.
- **Multi-Model Free AI Routing:** Cascading fallback across top free models (`qwen/qwen3.8-27b:free`, `google/gemma-4-31b-it:free`, `nvidia/nemotron-3.5-lightning:free`, `cohere/north-mini-code:free`, `openrouter/free`) and CodeCraft API fallback.
- **Progressive Disclosure:** 3-tier collapsible hints (Conceptual Nudge $\rightarrow$ Strategy $\rightarrow$ Code Skeleton).
- **Mastery Dashboard:** Aggregated report card, average score, and rank badge.

---

## 🚀 Quickstart Guide

### 1. Requirements
Ensure you have **Python 3.10+** and **Node.js 18+** installed.

```bash
# Verify installations
python --version
node --version
```

### 2. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 3. Launch Jupyter
```bash
jupyter lab
# or
jupyter notebook
```

Open `decorator_mastery_test.ipynb` and run the cells sequentially!

---

## ⚙️ Configuration (`config.yaml`)

Your API keys and model routing priorities are managed in `config.yaml`:

```yaml
ai_backend:
  primary: "openrouter"
  fallback: "codecraft"
  openrouter:
    api_key: "sk-or-v1-..."
    base_url: "https://openrouter.ai/api/v1"
    models:
      - "qwen/qwen3.8-27b:free"
      - "google/gemma-4-31b-it:free"
      - "nvidia/nemotron-3.5-lightning:free"
      - "cohere/north-mini-code:free"
      - "openrouter/free"
```

---

## 🧪 Testing the Harness

Run deterministic validation across all 10 questions:
```bash
python test_all_questions.py
```
