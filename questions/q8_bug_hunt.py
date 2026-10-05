"""
Question 8: arguments vs Rest Parameters Bug Hunt
Focus: Arrow function lexical scope, arguments shadowing, func.call vs func.apply, rest parameter best practices.
"""

Q8 = {
    "id": 8,
    "title": "Lexical Scope & Arguments Bug Hunt",
    "difficulty": "Advanced",
    "concepts": ["Arrow functions vs function keyword", "arguments shadowing", "Rest parameters (...args)", "Lexical this"],
    "description": """
### Problem Statement
A junior developer wrote the following buggy decorator intended to measure execution time and log all arguments and return values:

```javascript
// BUGGY IMPLEMENTATION:
function timeAndLog(fn) {
  return (...args) => {
    console.log("Calling with args:", arguments); // BUG 1: Arrow function uses enclosing arguments
    const start = Date.now();
    const result = fn.apply(this, arguments);    // BUG 2: 'this' is lexical (often undefined/global) and arguments is wrong
    const duration = Date.now() - start;
    return { result, duration, args };
  };
}
```

Fix the implementation in `fixedTimeAndLog(fn)` so that:
1. It works transparently when called as an **object method** (preserving the method caller as `this`).
2. It correctly captures and returns all passed arguments as a clean Array in `.args`.
3. It accurately invokes `fn` with the runtime `this` and arguments, returning an object: `{ result, duration, args }`.
4. It attaches a `.totalExecutionCount` property to the wrapper that tracks total times the wrapper was called.
""",
    "starter_code": """function fixedTimeAndLog(fn) {
  // TODO: Fix the lexical scope and arguments bugs
  function wrapper(...args) {
    
  }

  wrapper.totalExecutionCount = 0;
  return wrapper;
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "Arrow functions bind `this` and `arguments` lexically from where they are defined, NOT from where they are called. A method wrapper needs `function(...args)` to receive dynamic runtime `this`."
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "1. Use `function(...args)` for the wrapper.\n2. Increment `wrapper.totalExecutionCount++`.\n3. Measure `Date.now()`, execute `fn.apply(this, args)` or `fn.call(this, ...args)`.\n4. Return `{ result, duration, args }`."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function fixedTimeAndLog(fn) {
  function wrapper(...args) {
    wrapper.totalExecutionCount++;
    const start = Date.now();
    const result = fn.apply(this, args);
    const duration = Date.now() - start;
    return { result, duration, args };
  }
  wrapper.totalExecutionCount = 0;
  return wrapper;
}
```"""
        }
    ],
    "test_suite_js": """
await test('Correctly executes and captures method context & args', () => {
    const service = {
        multiplier: 3,
        compute(x, y) {
            return (x + y) * this.multiplier;
        }
    };

    service.compute = fixedTimeAndLog(service.compute);
    const report = service.compute(4, 6);

    assertEqual(report.result, 30, 'Proper this context maintained on method call');
    assertEqual(report.args, [4, 6], 'Arguments array correctly forwarded');
    assert(typeof report.duration === 'number', 'Duration is calculated');
    assertEqual(service.compute.totalExecutionCount, 1, 'Total execution count incremented');
});

await test('Works on variadic inputs', () => {
    function sum(...nums) {
        return nums.reduce((a, b) => a + b, 0);
    }
    const tracked = fixedTimeAndLog(sum);
    const res = tracked(1, 2, 3, 4, 5);

    assertEqual(res.result, 15);
    assertEqual(res.args, [1, 2, 3, 4, 5]);
    assertEqual(tracked.totalExecutionCount, 1);
});
""",
    "solution_code": """function fixedTimeAndLog(fn) {
  function wrapper(...args) {
    wrapper.totalExecutionCount++;
    const start = Date.now();
    const result = fn.apply(this, args);
    const duration = Date.now() - start;
    return { result, duration, args };
  }

  wrapper.totalExecutionCount = 0;
  return wrapper;
}""",
    "explanation": "Because regular function declarations define dynamic `this` based on the call-site and modern rest parameters (`...args`) produce actual Arrays (unlike the legacy array-like `arguments` object), replacing the arrow function solves both context loss and argument corruption."
}
