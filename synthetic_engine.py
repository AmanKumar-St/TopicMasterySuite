"""
SyntheticEngine: Autonomous procedural generation of progressive 10-tier diagnostic mastery suites
for ANY custom topic, domain, or framework without external dependency on remote LLM latency.
"""

import re
from typing import Any, Dict, List


def _clean_keywords(topic: str) -> List[str]:
    # Extract significant terms from topic
    words = re.findall(r"[A-Za-z0-9_-]+", topic)
    stopwords = {"and", "or", "the", "a", "an", "in", "on", "with", "without", "for", "to", "of", "etc", "etcetera"}
    cleaned = [w for w in words if w.lower() not in stopwords]
    return cleaned if cleaned else ["CoreConcept", "Process"]


def generate_synthetic_suite(topic: str) -> List[Dict[str, Any]]:
    """
    Generates 10 topic-tailored, progressive diagnostic challenges with fully functional
    JavaScript test suites, starter codes, and working reference solutions.
    """
    keywords = _clean_keywords(topic)
    primary_kw = keywords[0] if keywords else "Topic"
    secondary_kw = keywords[1] if len(keywords) > 1 else "Context"
    combined_title = " ".join(keywords[:3]).title()

    questions = [
        {
            "id": 1,
            "title": f"Fundamental Mechanics: {primary_kw} Parser & Formatter",
            "difficulty": "Fundamental",
            "concepts": [f"{primary_kw} core syntax", "Input normalization", "Data parsing"],
            "description": f"""
### Problem Statement
Build the core processor for **{topic}**.

Write a function `process{primary_kw}(input, options = {{}})` that normalizes the input data, extracts relevant `{primary_kw}` attributes, and returns a structured payload.

#### Requirements:
1. If `input` is a string, trim whitespace and return `{{ value: input.trim(), topic: '{primary_kw}', processed: true }}`.
2. If `options.tag` is provided, include `tag: options.tag` in the returned object.
3. If `input` is null or undefined, throw a `TypeError('Invalid input for {primary_kw}')`.
""",
            "starter_code": f"""function process{primary_kw}(input, options = {{}}) {{
  // TODO: Validate input and return structured {primary_kw} data
  
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": f"Check for null/undefined first before attempting to process `{primary_kw}`."},
                {"tier": 2, "title": "Approach Strategy", "content": "Throw TypeError for null/undefined. Return an object with value, topic, processed, and optional tag."},
                {"tier": 3, "title": "Code Skeleton", "content": f"```javascript\nfunction process{primary_kw}(input, options = {{}}) {{\n  if (input === null || input === undefined) throw new TypeError('Invalid input for {primary_kw}');\n  const res = {{ value: String(input).trim(), topic: '{primary_kw}', processed: true }};\n  if (options.tag) res.tag = options.tag;\n  return res;\n}}\n```"}
            ],
            "test_suite_js": f"""
await test('Processes string input with topic metadata', () => {{
    const res = process{primary_kw}('  sample data  ');
    assertEqual(res.value, 'sample data');
    assertEqual(res.topic, '{primary_kw}');
    assertEqual(res.processed, true);
}});

await test('Applies optional tag option', () => {{
    const res = process{primary_kw}('test', {{ tag: 'alpha' }});
    assertEqual(res.tag, 'alpha');
}});

await test('Throws TypeError on null/undefined', () => {{
    let threw = false;
    try {{
        process{primary_kw}(null);
    }} catch (e) {{
        threw = (e instanceof TypeError);
    }}
    assert(threw, 'Should throw TypeError for null input');
}});
""",
            "solution_code": f"""function process{primary_kw}(input, options = {{}}) {{
  if (input === null || input === undefined) {{
    throw new TypeError('Invalid input for {primary_kw}');
  }}
  const res = {{
    value: String(input).trim(),
    topic: '{primary_kw}',
    processed: true
  }};
  if (options.tag) {{
    res.tag = options.tag;
  }}
  return res;
}}""",
            "explanation": f"Core entry-point handler for {topic}, validating input boundaries and structuring normalized metadata."
        },
        {
            "id": 2,
            "title": f"State Tracking: {primary_kw} Activity Recorder",
            "difficulty": "Fundamental",
            "concepts": ["Closure encapsulation", "State logging", "Audit history"],
            "description": f"""
### Problem Statement
Create a recorder `create{primary_kw}Tracker()` to log and inspect all operations performed within the **{topic}** domain.

#### Requirements:
1. Returns an object with methods:
   - `record(action, payload)`: Appends an entry `{{ action, payload, timestamp: Date.now() }}` to internal history and returns total entries count.
   - `getHistory(actionFilter)`: Returns a shallow copy array of recorded entries (filtered by `action` if `actionFilter` is supplied).
   - `clear()`: Resets history and returns `0`.
""",
            "starter_code": f"""function create{primary_kw}Tracker() {{
  // TODO: Encapsulate private history and expose record, getHistory, clear
  
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": "Keep an array in the closure scope."},
                {"tier": 2, "title": "Approach Strategy", "content": "Use `filter` when `actionFilter` is provided, otherwise `slice()` for copy."},
                {"tier": 3, "title": "Code Skeleton", "content": f"```javascript\nfunction create{primary_kw}Tracker() {{\n  let history = [];\n  return {{\n    record(action, payload) {{\n      history.push({{ action, payload, timestamp: Date.now() }});\n      return history.length;\n    }},\n    getHistory(filter) {{\n      return filter ? history.filter(h => h.action === filter) : [...history];\n    }},\n    clear() {{\n      history = [];\n      return 0;\n    }}\n  }};\n}}\n```"}
            ],
            "test_suite_js": f"""
await test('Records actions and returns count', () => {{
    const tracker = create{primary_kw}Tracker();
    assertEqual(tracker.record('init', {{ id: 1 }}), 1);
    assertEqual(tracker.record('update', {{ id: 1, val: 'ok' }}), 2);
    assertEqual(tracker.getHistory().length, 2);
}});

await test('Filters history by action name', () => {{
    const tracker = create{primary_kw}Tracker();
    tracker.record('read', {{ key: 'a' }});
    tracker.record('write', {{ key: 'b' }});
    tracker.record('read', {{ key: 'c' }});
    assertEqual(tracker.getHistory('read').length, 2);
    assertEqual(tracker.getHistory('write').length, 1);
}});
""",
            "solution_code": f"""function create{primary_kw}Tracker() {{
  let history = [];
  return {{
    record(action, payload) {{
      history.push({{ action, payload, timestamp: Date.now() }});
      return history.length;
    }},
    getHistory(filter) {{
      return filter ? history.filter(h => h.action === filter) : [...history];
    }},
    clear() {{
      history = [];
      return 0;
    }}
  }};
}}""",
            "explanation": "Demonstrates closure-based state encapsulation for domain activity monitoring."
        },
        {
            "id": 3,
            "title": f"Validation & Schema: {primary_kw} Guard",
            "difficulty": "Intermediate",
            "concepts": ["Schema validation", "Type checking", "Error accumulation"],
            "description": f"""
### Problem Statement
Implement a schema validator `validate{primary_kw}Schema(target, schema)` to verify that entities in **{topic}** conform to required invariants.

#### Requirements:
1. `schema` is an object where keys are expected property names and values are type strings (`'string'`, `'number'`, `'boolean'`, `'function'`).
2. If `target` satisfies all types, return `{{ valid: true, errors: [] }}`.
3. If any required property is missing or has incorrect `typeof`, return `{{ valid: false, errors: ['missing or invalid <prop>'] }}`.
""",
            "starter_code": f"""function validate{primary_kw}Schema(target, schema) {{
  // TODO: Validate properties of target against schema definition
  
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": "Iterate over `Object.keys(schema)` and check `typeof target[key] === schema[key]`."},
                {"tier": 2, "title": "Approach Strategy", "content": "Handle non-object target early by reporting invalid target."},
                {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction validate(target, schema) {\n  const errors = [];\n  if (!target || typeof target !== 'object') return { valid: false, errors: ['Target is not an object'] };\n  for (const [k, t] of Object.entries(schema)) {\n    if (typeof target[k] !== t) errors.push(`Invalid field ${k}`);\n  }\n  return { valid: errors.length === 0, errors };\n}\n```"}
            ],
            "test_suite_js": f"""
await test('Validates matching schema successfully', () => {{
    const schema = {{ id: 'number', label: 'string', active: 'boolean' }};
    const entity = {{ id: 101, label: '{primary_kw} Unit', active: true }};
    const res = validate{primary_kw}Schema(entity, schema);
    assertEqual(res.valid, true);
    assertEqual(res.errors.length, 0);
}});

await test('Detects missing or mistyped properties', () => {{
    const schema = {{ count: 'number', name: 'string' }};
    const entity = {{ count: 'five', name: 'Test' }};
    const res = validate{primary_kw}Schema(entity, schema);
    assertEqual(res.valid, false);
    assert(res.errors.length > 0, 'Errors should list type mismatch');
}});
""",
            "solution_code": f"""function validate{primary_kw}Schema(target, schema) {{
  const errors = [];
  if (!target || typeof target !== 'object') {{
    return {{ valid: false, errors: ['Target must be an object'] }};
  }}
  for (const [key, expectedType] of Object.entries(schema)) {{
    if (typeof target[key] !== expectedType) {{
      errors.push(`Property '${{key}}' expected type ${{expectedType}}, got ${{typeof target[key]}}`);
    }}
  }}
  return {{ valid: errors.length === 0, errors }};
}}""",
            "explanation": "Validates data contracts and invariants necessary for predictable execution in complex workflows."
        },
        {
            "id": 4,
            "title": f"Async Coordination: {primary_kw} Task Queue",
            "difficulty": "Intermediate",
            "concepts": ["Async/Await", "Promise chaining", "Sequential execution"],
            "description": f"""
### Problem Statement
Write an async batch runner `run{primary_kw}Sequence(tasks, initialValue)` that executes a list of asynchronous tasks sequentially for **{topic}**.

#### Requirements:
1. `tasks` is an array of async functions `[task1, task2, ...]`.
2. Each task receives the output of the previous task (starting with `initialValue`).
3. Returns a Promise resolving to the final result after all tasks have completed in sequence.
4. If `tasks` is empty, resolves to `initialValue`.
""",
            "starter_code": f"""async function run{primary_kw}Sequence(tasks, initialValue) {{
  // TODO: Execute async tasks sequentially passing intermediate values
  
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": "Use a `for...of` loop with `await task(current)`."},
                {"tier": 2, "title": "Approach Strategy", "content": "Initialize `let current = initialValue;` then iterate over tasks awaiting each."},
                {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nasync function runSequence(tasks, initial) {\n  let current = initial;\n  for (const t of tasks) {\n    current = await t(current);\n  }\n  return current;\n}\n```"}
            ],
            "test_suite_js": f"""
await test('Executes async pipeline in sequential order', async () => {{
    const step1 = async (x) => x + 10;
    const step2 = async (x) => new Promise(r => setTimeout(() => r(x * 2), 10));
    const step3 = async (x) => `[{primary_kw}: ${{x}}]`;
    
    const result = await run{primary_kw}Sequence([step1, step2, step3], 5);
    // (5 + 10) * 2 = 30 -> '[{primary_kw}: 30]'
    assertEqual(result, '[{primary_kw}: 30]');
}});

await test('Handles empty task list', async () => {{
    const result = await run{primary_kw}Sequence([], 'unchanged');
    assertEqual(result, 'unchanged');
}});
""",
            "solution_code": f"""async function run{primary_kw}Sequence(tasks, initialValue) {{
  let current = initialValue;
  for (const task of tasks) {{
    current = await task(current);
  }}
  return current;
}}""",
            "explanation": "Guarantees ordered asynchronous lifecycle progression without race conditions."
        },
        {
            "id": 5,
            "title": f"Transformation Pipeline: Compose {combined_title}",
            "difficulty": "Intermediate",
            "concepts": ["Function composition", "Pure transformations", "Pipeline flow"],
            "description": f"""
### Problem Statement
Write a pipeline composer `compose{primary_kw}Pipeline(...transformers)` that combines multiple transformation functions into a single pipeline.

#### Requirements:
1. Returns a function `(input) => ...`
2. Passes `input` through each transformer from left to right.
3. If no transformers are supplied, returns the input as-is.
""",
            "starter_code": f"""function compose{primary_kw}Pipeline(...transformers) {{
  // TODO: Return a single composable pipeline function
  
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": "Use `reduce` across the `transformers` array."},
                {"tier": 2, "title": "Approach Strategy", "content": "Return `(input) => transformers.reduce((acc, fn) => fn(acc), input)`."},
                {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction compose(...transformers) {\n  return (input) => transformers.reduce((acc, fn) => fn(acc), input);\n}\n```"}
            ],
            "test_suite_js": f"""
await test('Pipes through multiple transformation steps', () => {{
    const trim = s => s.trim();
    const upper = s => s.toUpperCase();
    const wrap = s => `<<${{s}}>>`;
    
    const pipeline = compose{primary_kw}Pipeline(trim, upper, wrap);
    assertEqual(pipeline('  {primary_kw.lower()}  '), '<<{primary_kw.upper()}>>');
}});
""",
            "solution_code": f"""function compose{primary_kw}Pipeline(...transformers) {{
  return function(input) {{
    return transformers.reduce((acc, fn) => fn(acc), input);
  }};
}}""",
            "explanation": "Enables modular functional composition for clean, reusable domain transformations."
        },
        {
            "id": 6,
            "title": f"Property Immutability: {primary_kw} Frozen Registry",
            "difficulty": "Advanced",
            "concepts": ["Object.freeze", "Deep immutability", "Integrity enforcement"],
            "description": f"""
### Problem Statement
In **{topic}**, configuration and state snapshots must often be protected from unintended mutation.

Write `deepFreeze{primary_kw}(obj)` that recursively freezes an object and all nested objects/arrays.

#### Requirements:
1. Freezes `obj` using `Object.freeze`.
2. Recursively freezes all nested object and array properties.
3. Safely handles primitive values without throwing.
4. Returns the frozen object.
""",
            "starter_code": f"""function deepFreeze{primary_kw}(obj) {{
  // TODO: Recursively freeze obj and nested structures
  
  return obj;
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": "Check `if (obj === null || typeof obj !== 'object') return obj;` before freezing."},
                {"tier": 2, "title": "Approach Strategy", "content": "Call `Object.freeze(obj)`, then iterate `Object.keys(obj)` and recursively call `deepFreeze` on child objects."},
                {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction deepFreeze(obj) {\n  if (obj === null || typeof obj !== 'object') return obj;\n  Object.freeze(obj);\n  for (const key of Object.keys(obj)) {\n    deepFreeze(obj[key]);\n  }\n  return obj;\n}\n```"}
            ],
            "test_suite_js": f"""
await test('Deeply freezes nested structures', () => {{
    const config = {{
        topic: '{primary_kw}',
        settings: {{ mode: 'strict', retries: 3 }},
        items: [1, 2, {{ flag: true }}]
    }};
    const frozen = deepFreeze{primary_kw}(config);
    assertEqual(Object.isFrozen(frozen), true);
    assertEqual(Object.isFrozen(frozen.settings), true);
    assertEqual(Object.isFrozen(frozen.items), true);
    assertEqual(Object.isFrozen(frozen.items[2]), true);
}});
""",
            "solution_code": f"""function deepFreeze{primary_kw}(obj) {{
  if (obj === null || typeof obj !== 'object') {{
    return obj;
  }}
  Object.freeze(obj);
  for (const key of Object.keys(obj)) {{
    deepFreeze{primary_kw}(obj[key]);
  }}
  return obj;
}}""",
            "explanation": "Guarantees runtime tamper resistance across configuration states."
        },
        {
            "id": 7,
            "title": f"Configurable Factory: {primary_kw} Instance Builder",
            "difficulty": "Advanced",
            "concepts": ["Builder pattern", "Fluent API", "Immutable configuration"],
            "description": f"""
### Problem Statement
Design a fluent builder `create{primary_kw}Builder()` that configures and creates `{primary_kw}` execution nodes.

#### Requirements:
1. `builder.setName(name)`: Sets name and returns builder.
2. `builder.setParam(key, val)`: Sets custom parameter and returns builder.
3. `builder.build()`: Returns a sealed object `{{ name: string, params: object, execute() }}` where `execute()` returns `"${{name}} executing with params: ${{JSON.stringify(params)}}"`.
""",
            "starter_code": f"""function create{primary_kw}Builder() {{
  // TODO: Implement fluent builder with setName, setParam, build
  
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": "Maintain internal `name` and `params` dictionary in builder."},
                {"tier": 2, "title": "Approach Strategy", "content": "Return `this` from setter methods to enable chaining `builder.setName(...).setParam(...)`."},
                {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction createBuilder() {\n  let name = 'default';\n  const params = {};\n  return {\n    setName(n) { name = n; return this; },\n    setParam(k, v) { params[k] = v; return this; },\n    build() {\n      const p = { ...params };\n      return {\n        name,\n        params: p,\n        execute() { return `${name} executing with params: ${JSON.stringify(p)}`; }\n      };\n    }\n  };\n}\n```"}
            ],
            "test_suite_js": f"""
await test('Builds configured instance via fluent chaining', () => {{
    const instance = create{primary_kw}Builder()
        .setName('{primary_kw}Node')
        .setParam('env', 'production')
        .setParam('cluster', 4)
        .build();
        
    assertEqual(instance.name, '{primary_kw}Node');
    assertEqual(instance.params.env, 'production');
    assertEqual(instance.params.cluster, 4);
    assert(instance.execute().includes('{primary_kw}Node executing'), 'execute() output matches specification');
}});
""",
            "solution_code": f"""function create{primary_kw}Builder() {{
  let name = '{primary_kw}Default';
  const params = {{}};
  return {{
    setName(n) {{
      name = n;
      return this;
    }},
    setParam(k, v) {{
      params[k] = v;
      return this;
    }},
    build() {{
      const snapshotParams = {{ ...params }};
      const snapshotName = name;
      return {{
        name: snapshotName,
        params: snapshotParams,
        execute() {{
          return `${{snapshotName}} executing with params: ${{JSON.stringify(snapshotParams)}}`;
        }}
      }};
    }}
  }};
}}""",
            "explanation": "Fluent builder pattern decouples complex instance construction from operational logic."
        },
        {
            "id": 8,
            "title": f"Bug Hunt: {primary_kw} Memoization Edge Cases",
            "difficulty": "Advanced",
            "concepts": ["Memoization", "Object hashing", "Cache invalidation"],
            "description": f"""
### Problem Statement
The following memoizer function has a critical bug when caching calls with object parameters or different argument counts.

Fix `memoize{primary_kw}(fn)` so that:
1. It caches results based on all serialized arguments (`JSON.stringify(args)`).
2. It correctly distinguishes `fn(1, 2)` from `fn([1, 2])`.
3. It exposes a `.clear()` method on the returned memoized function to flush its cache.
""",
            "starter_code": f"""function memoize{primary_kw}(fn) {{
  // BUGGY: Only uses first argument as raw key
  const cache = {{}};
  const memoized = function(firstArg) {{
    if (cache[firstArg]) return cache[firstArg];
    const res = fn(firstArg);
    cache[firstArg] = res;
    return res;
  }};
  return memoized;
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": "Use `(...args)` to capture all arguments and `JSON.stringify(args)` as the cache key in a `Map`."},
                {"tier": 2, "title": "Approach Strategy", "content": "Attach `memoized.clear = () => cache.clear();` onto the returned function."},
                {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction memoize(fn) {\n  const cache = new Map();\n  const memoized = function(...args) {\n    const key = JSON.stringify(args);\n    if (cache.has(key)) return cache.get(key);\n    const result = fn.apply(this, args);\n    cache.set(key, result);\n    return result;\n  };\n  memoized.clear = () => cache.clear();\n  return memoized;\n}\n```"}
            ],
            "test_suite_js": f"""
await test('Correctly memoizes multi-arg functions and allows clearing', () => {{
    let callCount = 0;
    const add = (a, b) => {{ callCount++; return a + b; }};
    const memo = memoize{primary_kw}(add);
    
    assertEqual(memo(2, 3), 5);
    assertEqual(callCount, 1);
    assertEqual(memo(2, 3), 5);
    assertEqual(callCount, 1, 'Hits cache on identical args');
    
    memo.clear();
    assertEqual(memo(2, 3), 5);
    assertEqual(callCount, 2, 'Re-executes after cache clear');
}});
""",
            "solution_code": f"""function memoize{primary_kw}(fn) {{
  const cache = new Map();
  const memoized = function(...args) {{
    const key = JSON.stringify(args);
    if (cache.has(key)) {{
      return cache.get(key);
    }}
    const result = fn.apply(this, args);
    cache.set(key, result);
    return result;
  }};
  memoized.clear = () => cache.clear();
  return memoized;
}}""",
            "explanation": "Fixes argument serialization and provides explicit cache invalidation mechanisms."
        },
        {
            "id": 9,
            "title": f"Concurrency & Rate-Limiting: {primary_kw} Throttle",
            "difficulty": "Expert",
            "concepts": ["Throttling", "Timestamp windows", "Trailing edge calls"],
            "description": f"""
### Problem Statement
Implement a rate-limiter `throttle{primary_kw}(fn, limitMs)` for high-frequency events in **{topic}**.

#### Requirements:
1. Executes `fn` immediately on first invocation.
2. Ignores subsequent invocations within `limitMs` duration.
3. Forwards `this` and arguments properly.
""",
            "starter_code": f"""function throttle{primary_kw}(fn, limitMs) {{
  // TODO: Throttle execution of fn to once per limitMs
  
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": "Track `lastCallTime = 0` and compare `Date.now() - lastCallTime >= limitMs`."},
                {"tier": 2, "title": "Approach Strategy", "content": "If enough time passed, update `lastCallTime = Date.now()` and return `fn.apply(this, args)`."},
                {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction throttle(fn, limitMs) {\n  let last = 0;\n  return function(...args) {\n    const now = Date.now();\n    if (now - last >= limitMs) {\n      last = now;\n      return fn.apply(this, args);\n    }\n  };\n}\n```"}
            ],
            "test_suite_js": f"""
await test('Throttles rapid calls within time limit', async () => {{
    let count = 0;
    const trigger = throttle{primary_kw}(() => count++, 50);
    
    trigger();
    trigger();
    trigger();
    assertEqual(count, 1, 'Only first call executes immediately');
    
    await new Promise(r => setTimeout(r, 60));
    trigger();
    assertEqual(count, 2, 'Executes again after delay');
}});
""",
            "solution_code": f"""function throttle{primary_kw}(fn, limitMs) {{
  let lastCall = 0;
  return function(...args) {{
    const now = Date.now();
    if (now - lastCall >= limitMs) {{
      lastCall = now;
      return fn.apply(this, args);
    }}
  }};
}}""",
            "explanation": "Guarantees throughput control and prevents event flooding across high-frequency interfaces."
        },
        {
            "id": 10,
            "title": f"Diagnostic Challenge: {primary_kw} System Orchestrator",
            "difficulty": "Expert",
            "concepts": ["Orchestrator pattern", "Error recovery", "Telemetry dispatch", "Fallback execution"],
            "description": f"""
### Problem Statement
Construct a comprehensive resilient orchestrator `create{primary_kw}Orchestrator()` for the **{topic}** domain.

#### Requirements:
1. `orchestrator.register(name, handler)`: Registers a named task.
2. `orchestrator.execute(name, payload, fallbackHandler)`:
   - Attempts to run `handler(payload)`.
   - If `handler` succeeds, returns `{{ success: true, result, error: null }}`.
   - If `handler` throws and `fallbackHandler` is provided, runs `fallbackHandler(payload)` and returns `{{ success: true, result: fallbackResult, error: originalError.message, recovered: true }}`.
   - If `handler` throws without fallback, returns `{{ success: false, result: null, error: err.message }}`.
3. `orchestrator.getStats()`:
   - Returns `{{ total: number, successes: number, failures: number }}`.
""",
            "starter_code": f"""function create{primary_kw}Orchestrator() {{
  // TODO: Build orchestrator with register, execute, and getStats
  
}}""",
            "hints": [
                {"tier": 1, "title": "Conceptual Nudge", "content": "Store handlers in a `Map` and track counters for total, successes, failures in closure."},
                {"tier": 2, "title": "Approach Strategy", "content": "Wrap `execute` in a `try...catch`. Check for fallback in the catch block before registering a failure."},
                {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction createOrchestrator() {\n  const handlers = new Map();\n  let stats = { total: 0, successes: 0, failures: 0 };\n  return {\n    register(name, fn) { handlers.set(name, fn); },\n    execute(name, payload, fallback) {\n      stats.total++;\n      const fn = handlers.get(name);\n      if (!fn) {\n        stats.failures++;\n        return { success: false, result: null, error: `Handler not found: ${name}` };\n      }\n      try {\n        const res = fn(payload);\n        stats.successes++;\n        return { success: true, result: res, error: null };\n      } catch (err) {\n        if (typeof fallback === 'function') {\n          try {\n            const fbRes = fallback(payload);\n            stats.successes++;\n            return { success: true, result: fbRes, error: err.message, recovered: true };\n          } catch (fbErr) {\n            stats.failures++;\n            return { success: false, result: null, error: fbErr.message };\n          }\n        }\n        stats.failures++;\n        return { success: false, result: null, error: err.message };\n      }\n    },\n    getStats() { return { ...stats }; }\n  };\n}\n```"}
            ],
            "test_suite_js": f"""
await test('Executes registered tasks and updates stats', () => {{
    const orch = create{primary_kw}Orchestrator();
    orch.register('format', (d) => `[{primary_kw}: ${{d.val}}]`);
    
    const res = orch.execute('format', {{ val: 'active' }});
    assertEqual(res.success, true);
    assertEqual(res.result, '[{primary_kw}: active]');
    
    const stats = orch.getStats();
    assertEqual(stats.total, 1);
    assertEqual(stats.successes, 1);
}});

await test('Recovers via fallback handler on primary failure', () => {{
    const orch = create{primary_kw}Orchestrator();
    orch.register('failing', () => {{ throw new Error('Primary failed'); }});
    
    const res = orch.execute('failing', {{ val: 123 }}, () => 'fallback-ok');
    assertEqual(res.success, true);
    assertEqual(res.result, 'fallback-ok');
    assertEqual(res.recovered, true);
}});
""",
            "solution_code": f"""function create{primary_kw}Orchestrator() {{
  const handlers = new Map();
  const stats = {{ total: 0, successes: 0, failures: 0 }};
  return {{
    register(name, fn) {{
      handlers.set(name, fn);
    }},
    execute(name, payload, fallback) {{
      stats.total++;
      const fn = handlers.get(name);
      if (!fn) {{
        stats.failures++;
        return {{ success: false, result: null, error: `Handler '${{name}}' not found` }};
      }}
      try {{
        const res = fn(payload);
        stats.successes++;
        return {{ success: true, result: res, error: null }};
      }} catch (err) {{
        if (typeof fallback === 'function') {{
          try {{
            const fbRes = fallback(payload);
            stats.successes++;
            return {{ success: true, result: fbRes, error: err.message, recovered: true }};
          }} catch (fbErr) {{
            stats.failures++;
            return {{ success: false, result: null, error: fbErr.message }};
          }}
        }}
        stats.failures++;
        return {{ success: false, result: null, error: err.message }};
      }}
    }},
    getStats() {{
      return {{ ...stats }};
    }}
  }};
}}""",
            "explanation": f"Complete diagnostic pattern demonstrating resilient task execution and telemetry for {topic}."
        }
    ]
    return questions
