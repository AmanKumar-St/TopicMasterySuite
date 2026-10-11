# 🎯 Topic Mastery Suite

Master **any topic** you just learned — entirely inside a Jupyter notebook.

No hardcoded questions. No templates. No deterministic answer keys. Everything is generated and graded live by an LLM.

## How it works

1. **Enter your topic** — *"Python decorators"*, *"the Krebs cycle"*, *"French Revolution"*, anything.
2. **The AI analyzes it** — identifies the subject/language, and if the topic is too broad, **asks you clarifying questions** before continuing.
3. **Run `new_question()`** — a fresh, unique question is generated and an **empty answer cell appears below it**.
4. **Write your answer in that cell and run it** — the AI grades it instantly:
   - ✅ correct / 🟡 partially correct / ❌ incorrect
   - score out of 10, detailed feedback, **and a model answer** to study from
5. Repeat — every question is **guaranteed unique** (session history is persisted in `.topic_mastery_history.json`, so no repeats even across sessions).

## Quickstart

```bash
pip install -r requirements.txt
cp .env.example .env   # add ONE API key (or run Ollama locally — no key needed)
jupyter notebook       # open TopicMastery.ipynb and run the cells top to bottom
```

## LLM providers (auto-detected, in this order)

| Provider | Env var | Notes |
|---|---|---|
| OpenRouter | `OPENROUTER_API_KEY` | Free models available, automatic fallback across them |
| Google Gemini | `GEMINI_API_KEY` | Free tier available |
| OpenAI | `OPENAI_API_KEY` | Defaults to `gpt-4o-mini` |
| Ollama | *(none)* | Local & free — just `ollama serve` |

## Notebook commands

| Command | What it does |
|---|---|
| `new_question()` | Generates a unique question + opens an empty answer cell |
| `new_question("hard")` | Force a difficulty (`easy` / `medium` / `hard` / `auto`) |
| `check_answer(my_answer)` | AI grades your answer (already in the answer cell) |
| `hint()` | Socratic hint for the current question |
| `session_report()` | Scorecard for the session |

## Files

```
TopicMastery.ipynb          ← the notebook (start here)
topic_mastery_engine.py     ← the LLM engine (analysis, generation, evaluation)
requirements.txt
.env.example
```

## Why no tests / no question bank?

That's the point. The previous version of this project had 10 hardcoded JavaScript questions with deterministic Node.js tests. This rebuild deletes that entire approach: question generation and answer evaluation are both pure LLM calls, guided by prompts and a repetition-guard history file — so the suite works for **any subject**, not just one programming topic.
