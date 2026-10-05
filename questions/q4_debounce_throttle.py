"""
Question 4: Debounce vs Throttle Analysis & Implementation
Focus: Asynchronous decorators, timer management, argument capture, `this` retention across async callbacks.
"""

Q4 = {
    "id": 4,
    "title": "Debounce with Context Preservation",
    "difficulty": "Intermediate",
    "concepts": ["Debounce pattern", "setTimeout & clearTimeout", "Context preservation in async callbacks", "Trailing execution"],
    "description": """
### Problem Statement
Implement a `debounce(func, ms)` decorator that delays invoking `func` until after `ms` milliseconds have elapsed since the last time the debounced function was invoked.

#### Requirements:
1. Every call to the debounced function resets the countdown timer.
2. When the timer finally elapses, `func` must be called with the **exact context (`this`)** and **arguments** from the *most recent* invocation.
3. If called multiple times within the delay period, only the very last call's arguments and context are forwarded to `func`.
4. The debounced wrapper must expose a `.cancel()` method that clears any pending timer.
""",
    "starter_code": """function debounce(func, ms) {
  let timeoutId = null;

  function wrapper(...args) {
    // TODO: Implement debouncing with timer reset and context preservation
  }

  // TODO: Add wrapper.cancel() method
  
  return wrapper;
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "In an asynchronous callback inside `setTimeout`, what is `this`? You must capture the outer `this` (e.g., in a variable or using an arrow function closure) so it isn't lost when the timer fires."
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "Inside `wrapper`, call `clearTimeout(timeoutId)` first. Then assign `timeoutId = setTimeout(() => { func.apply(this, args); }, ms)`. Define `wrapper.cancel = () => clearTimeout(timeoutId)`."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function debounce(func, ms) {
  let timeoutId = null;

  function wrapper(...args) {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(() => {
      func.apply(this, args);
      timeoutId = null;
    }, ms);
  }

  wrapper.cancel = function() {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
  };

  return wrapper;
}
```"""
        }
    ],
    "test_suite_js": """
await test('Debounces rapid calls and executes only the last one', async () => {
    let callHistory = [];
    const fn = debounce((val) => {
        callHistory.push(val);
    }, 50);

    fn(1);
    fn(2);
    fn(3);

    assertEqual(callHistory.length, 0, 'No immediate execution');
    await new Promise(r => setTimeout(r, 70));
    assertEqual(callHistory, [3], 'Only the last invocation executed');
});

await test('Preserves `this` context when invoked as an object method', async () => {
    let executedContext = null;
    const worker = {
        name: 'DebounceWorker',
        run: debounce(function(action) {
            executedContext = this.name + ':' + action;
        }, 30)
    };

    worker.run('task-A');
    worker.run('task-B');

    await new Promise(r => setTimeout(r, 50));
    assertEqual(executedContext, 'DebounceWorker:task-B', 'Preserved object instance this context');
});

await test('Cancel method clears pending execution', async () => {
    let called = false;
    const fn = debounce(() => { called = true; }, 40);
    fn();
    fn.cancel();
    await new Promise(r => setTimeout(r, 60));
    assertEqual(called, false, 'Execution was successfully cancelled');
});
""",
    "solution_code": """function debounce(func, ms) {
  let timeoutId = null;

  function wrapper(...args) {
    if (timeoutId) {
      clearTimeout(timeoutId);
    }
    timeoutId = setTimeout(() => {
      func.apply(this, args);
      timeoutId = null;
    }, ms);
  }

  wrapper.cancel = function() {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
  };

  return wrapper;
}""",
    "explanation": "Because arrow functions capture `this` lexically from their enclosing execution context, `() => func.apply(this, args)` retains both the exact object context and the arguments of the latest invocation."
}
