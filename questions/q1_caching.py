"""
Question 1: Transparent Caching with Context
Focus: func.call / apply, preserving `this`, closure caching, multi-argument hashing.
"""

Q1 = {
    "id": 1,
    "title": "Transparent Caching with Context",
    "difficulty": "Fundamental",
    "concepts": ["func.call() / func.apply()", "this context forwarding", "Closure-based cache", "Multi-argument hashing"],
    "description": """
### Problem Statement
Write a decorator function `cachingDecorator(func, hashFn)` that wraps any function or object method and caches its return values in a `Map`.

#### Requirements:
1. When the wrapped function is invoked with arguments that have already been computed, it must return the cached value immediately without invoking `func` again.
2. **Context Preservation**: It MUST correctly preserve the `this` context when invoked as an object method (e.g. `obj.method(...)`).
3. **Multi-Argument & Hash Key**: If a custom `hashFn` is passed, use `hashFn(...args)` to determine the cache key. If `hashFn` is omitted, use `JSON.stringify(args)`.
4. The cache must remain encapsulated within the wrapper closure.
""",
    "starter_code": """function cachingDecorator(func, hashFn) {
  const cache = new Map();

  return function(...args) {
    // TODO: Implement transparent caching with proper context forwarding
    
  };
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "When a function is called as an object method (`worker.slow(x)`), what happens to `this` if you just do `func(...args)` instead of `func.call(this, ...args)`?"
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "1. Compute the cache key using `hashFn ? hashFn(...args) : JSON.stringify(args)`.\n2. Check `cache.has(key)`. If true, return `cache.get(key)`.\n3. If false, invoke `func.call(this, ...args)` and store the result in the cache."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function cachingDecorator(func, hashFn) {
  const cache = new Map();
  return function(...args) {
    const key = hashFn ? hashFn.apply(this, args) : JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = func.call(this, ...args);
    cache.set(key, result);
    return result;
  };
}
```"""
        }
    ],
    "test_suite_js": """
await test('Basic caching on standalone function', () => {
    let callCount = 0;
    function add(a, b) {
        callCount++;
        return a + b;
    }
    const cachedAdd = cachingDecorator(add);
    assertEqual(cachedAdd(2, 3), 5, 'First call returns sum');
    assertEqual(callCount, 1, 'add invoked once');
    assertEqual(cachedAdd(2, 3), 5, 'Second call returns cached sum');
    assertEqual(callCount, 1, 'add NOT invoked again on cache hit');
    assertEqual(cachedAdd(3, 4), 7, 'Different args return correct sum');
    assertEqual(callCount, 2, 'add invoked on new args');
});

await test('Preserves object context (`this`)', () => {
    let callCount = 0;
    const worker = {
        multiplier: 10,
        calculate(x, y) {
            callCount++;
            return (x + y) * this.multiplier;
        }
    };

    worker.calculate = cachingDecorator(worker.calculate);
    assertEqual(worker.calculate(1, 2), 30, 'Correct result using object multiplier');
    assertEqual(callCount, 1);
    assertEqual(worker.calculate(1, 2), 30, 'Cached result preserves context computation');
    assertEqual(callCount, 1);
});

await test('Custom hash function support', () => {
    let calls = 0;
    function greet(user) {
        calls++;
        return `Hello ${user.name}!`;
    }
    const cachedGreet = cachingDecorator(greet, u => u.id);
    assertEqual(cachedGreet({ id: 101, name: 'Alice' }), 'Hello Alice!');
    assertEqual(calls, 1);
    assertEqual(cachedGreet({ id: 101, name: 'Alice (updated)' }), 'Hello Alice!', 'Hits cache based on user.id key');
    assertEqual(calls, 1);
});
""",
    "solution_code": """function cachingDecorator(func, hashFn) {
  const cache = new Map();

  return function(...args) {
    const key = hashFn ? hashFn.apply(this, args) : JSON.stringify(args);
    if (cache.has(key)) {
      return cache.get(key);
    }
    const result = func.call(this, ...args);
    cache.set(key, result);
    return result;
  };
}""",
    "explanation": "By returning a regular function (not an arrow function, or forwarding `this` explicitly), we capture the runtime `this` at call time. `func.call(this, ...args)` or `func.apply(this, args)` transparently executes the original logic as if the decorator wasn't there."
}
