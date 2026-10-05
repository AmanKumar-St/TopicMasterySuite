"""
Question 2: Spy Decorator with Metadata
Focus: Decorator properties, func.apply / func.call, capturing call history, arguments forwarding.
"""

Q2 = {
    "id": 2,
    "title": "Spy Decorator with Call History",
    "difficulty": "Fundamental",
    "concepts": ["Decorator metadata properties", "Function object augmentation", "func.apply() forwarding", "Historical call logging"],
    "description": """
### Problem Statement
Create a decorator `spy(func)` that records all calls to the function and their arguments on a property `wrapper.calls`.

#### Requirements:
1. The returned wrapper function must execute `func` with the exact context (`this`) and arguments supplied.
2. The wrapper must have a `.calls` property which is an Array of arrays, where each inner array contains the arguments passed during that specific invocation (e.g. `[[1, 2], [3, 4]]`).
3. The wrapper must return whatever value `func` returns.
4. Calling `wrapper.calls.length` should accurately reflect the total number of invocations.
""",
    "starter_code": """function spy(func) {
  function wrapper(...args) {
    // TODO: Record args into wrapper.calls and forward execution
  }

  // TODO: Initialize wrapper metadata
  
  return wrapper;
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "Functions in JavaScript are first-class objects. You can attach custom properties directly to the `wrapper` function, like `wrapper.calls = []`."
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "Initialize `wrapper.calls = []` before returning the wrapper. Inside the wrapper body, push `args` (or a shallow copy of arguments) into `wrapper.calls` before invoking `func.apply(this, args)`."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function spy(func) {
  function wrapper(...args) {
    wrapper.calls.push(args);
    return func.apply(this, args);
  }
  wrapper.calls = [];
  return wrapper;
}
```"""
        }
    ],
    "test_suite_js": """
await test('Records argument history and return values', () => {
    function multiply(a, b) {
        return a * b;
    }
    const spied = spy(multiply);
    assertEqual(spied.calls, [], 'Initial calls array is empty');
    
    const r1 = spied(2, 3);
    assertEqual(r1, 6, 'Returns correct calculation');
    assertEqual(spied.calls.length, 1, 'One call logged');
    assertEqual(spied.calls[0], [2, 3], 'Arguments logged correctly');

    const r2 = spied(4, 5);
    assertEqual(r2, 20);
    assertEqual(spied.calls.length, 2);
    assertEqual(spied.calls[1], [4, 5]);
});

await test('Preserves method context on objects', () => {
    const user = {
        name: 'John',
        say(phrase) {
            return `${this.name}: ${phrase}`;
        }
    };
    user.say = spy(user.say);
    assertEqual(user.say('Hello'), 'John: Hello');
    assertEqual(user.say.calls[0], ['Hello']);
});
""",
    "solution_code": """function spy(func) {
  function wrapper(...args) {
    wrapper.calls.push(args);
    return func.apply(this, args);
  }

  wrapper.calls = [];
  return wrapper;
}""",
    "explanation": "Because JavaScript functions are objects, attaching properties like `wrapper.calls` directly to the function reference gives callers introspection capabilities while maintaining complete transparency during execution."
}
