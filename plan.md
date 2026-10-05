# JavaScript Decorators & call/apply - Jupyter Notebook Test Suite
## Comprehensive Implementation Plan

---

## Project Overview

Create an interactive Jupyter Notebook that tests deep understanding of JavaScript decorators, `call`/`apply`, and function forwarding through 10 carefully designed, progressive questions with AI-powered answer evaluation using OpenRouter + CodeCraft model routing, running on Python kernel with Node.js subprocess execution.

---

## Technical Architecture

### AI Backend: OpenRouter + CodeCraft Router
```
Student Answer -> OpenRouter (primary)
                      |
                      +-> deepseek-coder (code-specialized)
                      +-> codellama:7b (fast, cheap)
                      +-> gpt-4o-mini (reasoning fallback)
                      |
                      v (if primary fails)
                 CodeCraft Router
                      |
                      +-> Specialized code evaluation models
```

**Configuration**: `temperature=0.1`, `max_tokens=1500`, structured JSON output

### Kernel: Python + Node.js Subprocess
```python
class JSEvaluator:
    def evaluate(self, student_code: str, test_code: str) -> dict:
        # Write to temp file, execute via node, parse JSON output
        # Sandboxed, timeout=10s, auto-cleanup
```

**Advantages**: Works anywhere Python + Node.js installed, no kernel install complexity, easy debugging

---

## The 10 Questions (Progressive Difficulty)

| # | Title | Type | Core Concepts |
|---|-------|------|---------------|
| 1 | Transparent Caching with Context | Implementation | `call`, `this` forwarding, closure, multi-arg |
| 2 | Spy Decorator with Metadata | Implementation | Decorator properties, `apply`, `arguments` vs rest |
| 3 | Method Borrowing Deep-Dive | Conceptual + Code | `arguments`, `[].join.call()`, spec behavior |
| 4 | Debounce vs Throttle Analysis | Conceptual + Implementation | Timer edge cases, leading/trailing, argument capture |
| 5 | Decorator Composition Order | Problem Solving | Wrapper nesting, interception order, timing |
| 6 | Preserving Function Properties | Advanced | `Proxy`, descriptors, `Object.getOwnPropertyDescriptors` |
| 7 | Curried Decorator Factory | Advanced Pattern | Factory pattern, currying, composition, config |
| 8 | `arguments` vs Rest Parameters Bug Hunt | Debugging | Arrow functions, `setTimeout` context, subtle bugs |
| 9 | Rate-Limited API Client | Integration | Async/await, Promise queue, sliding window |
| 10 | "Lost `this`" Diagnostic Challenge | Debugging | Chained decorators, class methods, 5 distinct bugs |

---

## Notebook Structure Per Question

```
+-------------------------------------------------------------+
| MARKDOWN CELL: Question (problem statement, code)           |
+-------------------------------------------------------------+
| MARKDOWN CELL: Progressive Hints (collapsible sections)     |
+-------------------------------------------------------------+
| CODE CELL: User Answer Area (empty, ready for input)        |
+-------------------------------------------------------------+
| CODE CELL: AI Evaluation Runner (auto-executes on run)      |
+-------------------------------------------------------------+
| MARKDOWN CELL: Solution Reveal (hidden, toggle button)      |
+-------------------------------------------------------------+
```

### Hint System (Three-Tier Progressive Disclosure)
```markdown
<details><summary>Hint 1: Conceptual Nudge</summary>
Think about how `func.call(this, ...args)` differs from `func(...args)`.
</details>

<details><summary>Hint 2: Approach Strategy</summary>
Your wrapper needs to capture `this`, forward correctly, store result.
</details>

<details><summary>Hint 3: Code Skeleton</summary>

```javascript
function yourDecorator(fn) {
  return function(...args) {
    const context = this;
    const result = fn.call(context, ...args);
    // decorator logic here
    return result;
  };
}
```
</details>
```

---

## AI Evaluation Pipeline

### Deterministic Tests First (Always Run)
```javascript
// Embedded test cases per question
const testCases = [
  {name: "Basic caching works", setup: "...", test: "...", hidden: false},
  {name: "Context preserved with call", setup: "...", test: "...", hidden: true}
];
```

### AI Evaluator Prompt Template
```python
EVALUATION_PROMPT = """
You are an expert JavaScript instructor evaluating a student's answer.

QUESTION: {question_text}
STUDENT_ANSWER: {student_code_or_explanation}
EXPECTED_CONCEPTS: {key_concepts_list}
TEST_RESULTS: {deterministic_test_output}

Return JSON:
{
  "verdict": "correct" | "partially_correct" | "incorrect",
  "score": 0-100,
  "explanation": "Clear explanation of what is right/wrong",
  "key_insight": "The one concept they missed or nailed",
  "next_steps": "Specific guidance for improvement"
}
"""
```

### Scoring System
- **0-100 graded** with three tiers: `correct` (>=70), `partially_correct` (40-69), `incorrect` (<40)
- Solution reveal: **manual button + auto after 3 failed attempts**

---

## File Structure & Deliverables

```
E:\Projects\LearningExercises\
├── decorator_mastery_test.ipynb      # Main notebook (Python kernel)
├── js_evaluator.py                   # Node.js subprocess wrapper
├── ai_evaluator.py                   # OpenRouter + CodeCraft client
├── config.yaml                       # API keys, model routing, thresholds
├── requirements.txt                  # Python dependencies
├── questions/
│   ├── __init__.py
│   ├── q1_caching.py                # Question 1: tests, prompt, solution
│   ├── q2_spy.py                    # Question 2: tests, prompt, solution
│   ├── q3_method_borrowing.py       # Question 3: tests, prompt, solution
│   ├── q4_debounce_throttle.py      # Question 4: tests, prompt, solution
│   ├── q5_composition.py            # Question 5: tests, prompt, solution
│   ├── q6_properties.py             # Question 6: tests, prompt, solution
│   ├── q7_factory.py                # Question 7: tests, prompt, solution
│   ├── q8_bug_hunt.py               # Question 8: tests, prompt, solution
│   ├── q9_rate_limit.py             # Question 9: tests, prompt, solution
│   └── q10_diagnostic.py            # Question 10: tests, prompt, solution
└── README.md                         # Setup, config, usage guide
```

---

## Configuration (config.yaml)

```yaml
ai_backend:
  primary: "openrouter"
  fallback: "codecraft"
  openrouter:
    api_key: "${OPENROUTER_API_KEY}"
    base_url: "https://openrouter.ai/api/v1"
    models:
      - "deepseek/deepseek-coder"
      - "meta-llama/codellama-7b-instruct"
      - "openai/gpt-4o-mini"
  codecraft:
    api_key: "${CODECRAFT_API_KEY}"
    base_url: "https://api.codecraft.ai/v1"

evaluation:
  temperature: 0.1
  max_tokens: 1500
  passing_score: 70
  partial_score_min: 40
  max_attempts_before_reveal: 3

notebook:
  kernel: "python3"
  node_path: "node"
  timeout_seconds: 10
```

---

## Python Dependencies (requirements.txt)

```
openai>=1.0.0          # OpenRouter compatible
pyyaml>=6.0            # Config parsing
jupyter>=1.0           # Notebook runtime
ipywidgets>=8.0        # Interactive hint toggles (optional)
nbformat>=5.0          # Notebook validation
```

---

## Implementation Phases

### Phase 1: Environment & Core Infrastructure (Day 1-2)
- [ ] Create `config.yaml` template with env var placeholders
- [ ] Build `js_evaluator.py` - Node.js subprocess with timeout/sandbox
- [ ] Build `ai_evaluator.py` - OpenRouter client with model fallback chain
- [ ] Build `Question` base class with render/evaluate interface
- [ ] Verify Python + Node.js execution works end-to-end

### Phase 2: Questions 1-3 (Fundamentals) (Day 3-4)
- [ ] Q1: Transparent Caching - tests, AI prompt, solution
- [ ] Q2: Spy Decorator - tests, AI prompt, solution
- [ ] Q3: Method Borrowing - conceptual explanation + code, AI prompt, solution
- [ ] Validate deterministic tests pass for all three

### Phase 3: Questions 4-6 (Advanced Patterns) (Day 5-6)
- [ ] Q4: Debounce vs Throttle - implementation + behavioral analysis
- [ ] Q5: Decorator Composition - prediction + verification tests
- [ ] Q6: Function Properties - Proxy + Object.defineProperties approaches

### Phase 4: Questions 7-10 (Expert/Integration) (Day 7-8)
- [ ] Q7: Curried Factory - configurable decorator system
- [ ] Q8: Bug Hunt - 4 distinct bug scenarios with fixes
- [ ] Q9: Rate-Limited API - async decorator with Promise queue
- [ ] Q10: Diagnostic Challenge - 5 bugs in chained decorators

### Phase 5: Notebook Assembly & Polish (Day 9-10)
- [ ] Generate `.ipynb` with all cells, metadata, CSS/JS for hints
- [ ] Embed `js_evaluator` and `ai_evaluator` as notebook initialization cells
- [ ] Add navigation, progress tracking (localStorage)
- [ ] Test end-to-end in Jupyter Classic + JupyterLab
- [ ] Create `README.md` with setup instructions

---

## Verification Strategy

### Automated Checks
| Check | Tool | Command |
|-------|------|---------|
| Notebook JSON valid | `nbformat` | `python -m nbformat.validate notebook.ipynb` |
| All code executable | Python kernel | `jupyter nbconvert --execute notebook.ipynb` |
| Deterministic tests pass | Custom runner | `python -m pytest questions/` |
| AI evaluator returns valid JSON | Schema validation | Unit tests in `ai_evaluator.py` |

### Manual QA Checklist
- [ ] Each question renders correctly in Jupyter Classic + JupyterLab
- [ ] Hints expand/collapse properly (markdown `<details>`)
- [ ] Solution reveal works (toggle button)
- [ ] AI evaluation triggers on answer cell execution
- [ ] Feedback displays clearly (color-coded: green/yellow/red)
- [ ] Progress persists across sessions (localStorage)
- [ ] Works with Node.js 18+, 20+, 22+

---

## Model Routing Logic (OpenRouter)

```python
MODEL_CHAIN = [
    {"model": "deepseek/deepseek-coder", "max_tokens": 1500, "priority": 1},
    {"model": "meta-llama/codellama-7b-instruct", "max_tokens": 1500, "priority": 2},
    {"model": "openai/gpt-4o-mini", "max_tokens": 1500, "priority": 3},
]

async def evaluate_with_fallback(prompt: str) -> dict:
    for model_config in MODEL_CHAIN:
        try:
            response = await openrouter_chat(model_config, prompt)
            return parse_json_response(response)
        except Exception as e:
            log.warning(f"Model {model_config['model']} failed: {e}")
            continue
    # Final fallback to CodeCraft
    return await codecraft_evaluate(prompt)
```

---

## Estimated Timeline

| Week | Focus | Deliverable |
|------|-------|-------------|
| 1 | Setup + Core Infra | Working test runner, AI evaluator with fallback |
| 2 | Questions 1-5 | Fundamental through composition questions |
| 3 | Questions 6-10 | Advanced patterns, debugging, integration |
| 4 | Assembly + Polish | Complete notebook, docs, fallback modes |

**Total Estimated Effort**: ~25-30 hours

---

## Key Decisions Confirmed

| Decision | Choice |
|----------|--------|
| AI Backend | OpenRouter (primary) + CodeCraft (fallback) |
| Models | deepseek-coder, codellama-7b, gpt-4o-mini via OpenRouter |
| Kernel | Python 3 + Node.js subprocess |
| Notebook Format | `.ipynb` (rich rendering) |
| Scoring | Graded 0-100 with partial credit tiers |
| Solution Reveal | Manual button + auto after 3 failures |
| Hint System | Markdown `<details>` collapsible (3 tiers) |

---

## Next Steps

1. **User provides**: OpenRouter API key, CodeCraft API access confirmation
2. **Initialize**: Create project structure, `config.yaml`, `requirements.txt`
3. **Begin Phase 1**: Core infrastructure (`js_evaluator.py`, `ai_evaluator.py`)
4. **Iterative delivery**: Questions implemented in batches with verification

---

*Plan saved as `plan.md` - Ready for implementation phase upon confirmation.*
