"""
Question 7: Curried Decorator Factory
Focus: Decorator factories, currying, configurable execution policies, asynchronous retry mechanics.
"""

Q7 = {
    "id": 7,
    "title": "Curried Retry Decorator Factory",
    "difficulty": "Advanced",
    "concepts": ["Decorator factory pattern", "Currying / partial application", "Async retry logic with backoff", "Error interception"],
    "description": """
### Problem Statement
Write a configurable decorator factory `retryDecorator(options)` that wraps asynchronous functions to automatically retry upon failure.

#### Requirements:
1. `options` is an object: `{ maxRetries = 3, delayMs = 0, shouldRetry = (err) => true }`.
2. When the decorated function is invoked, if it rejects/throws, it should retry up to `maxRetries` times.
3. If `delayMs > 0`, wait `delayMs` before each subsequent retry attempt.
4. If `shouldRetry(err)` returns `false`, do not retry—immediately throw the error.
5. If all retries are exhausted, reject with the error thrown on the final attempt.
6. Must preserve `this` context and all arguments across retry attempts.
""",
    "starter_code": """function retryDecorator(options = {}) {
  const { maxRetries = 3, delayMs = 0, shouldRetry = () => true } = options;

  return function(func) {
    return async function(...args) {
      // TODO: Implement async retry loop with delay and context preservation
      
    };
  };
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "A decorator factory returns a decorator function `(func) => wrapper`, which in turn returns the actual wrapper function `async function(...args) { ... }`."
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "Use a `for` loop from `attempt = 0` to `maxRetries`. In a `try/catch` block, `await func.apply(this, args)`. In `catch (err)`, check if `attempt < maxRetries && shouldRetry(err)`. If so, `await new Promise(r => setTimeout(r, delayMs))`. Otherwise, rethrow `err`."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function retryDecorator(options = {}) {
  const { maxRetries = 3, delayMs = 0, shouldRetry = () => true } = options;

  return function(func) {
    return async function(...args) {
      let lastErr;
      for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
          return await func.apply(this, args);
        } catch (err) {
          lastErr = err;
          if (attempt >= maxRetries || !shouldRetry(err)) {
            throw err;
          }
          if (delayMs > 0) {
            await new Promise(r => setTimeout(r, delayMs));
          }
        }
      }
      throw lastErr;
    };
  };
}
```"""
        }
    ],
    "test_suite_js": """
await test('Retries until success within limit', async () => {
    let attempts = 0;
    const fetchProfile = async (id) => {
        attempts++;
        if (attempts < 3) throw new Error('Network error');
        return { id, name: 'Alice' };
    };

    const withRetry = retryDecorator({ maxRetries: 3, delayMs: 10 })(fetchProfile);
    const result = await withRetry(42);

    assertEqual(result, { id: 42, name: 'Alice' });
    assertEqual(attempts, 3, 'Took 3 attempts to succeed');
});

await test('Fails if maxRetries exceeded', async () => {
    let attempts = 0;
    const failAlways = async () => {
        attempts++;
        throw new Error('Permanent failure');
    };

    const withRetry = retryDecorator({ maxRetries: 2, delayMs: 5 })(failAlways);
    let threw = false;
    try {
        await withRetry();
    } catch (e) {
        threw = true;
        assertEqual(e.message, 'Permanent failure');
    }
    assertEqual(threw, true, 'Error thrown when retries exhausted');
    assertEqual(attempts, 3, 'Initial call + 2 retries = 3 attempts total');
});

await test('Respects shouldRetry filter condition', async () => {
    let attempts = 0;
    const criticalError = async () => {
        attempts++;
        const err = new Error('Unauthorized 401');
        err.status = 401;
        throw err;
    };

    const withRetry = retryDecorator({
        maxRetries: 3,
        shouldRetry: (err) => err.status !== 401
    })(criticalError);

    let caught = false;
    try {
        await withRetry();
    } catch (e) {
        caught = true;
    }
    assertEqual(caught, true);
    assertEqual(attempts, 1, 'Did not retry on fatal 401 status');
});
""",
    "solution_code": """function retryDecorator(options = {}) {
  const { maxRetries = 3, delayMs = 0, shouldRetry = () => true } = options;

  return function(func) {
    return async function(...args) {
      let lastErr;
      for (let attempt = 0; attempt <= maxRetries; attempt++) {
        try {
          return await func.apply(this, args);
        } catch (err) {
          lastErr = err;
          if (attempt >= maxRetries || !shouldRetry(err)) {
            throw err;
          }
          if (delayMs > 0) {
            await new Promise(r => setTimeout(r, delayMs));
          }
        }
      }
      throw lastErr;
    };
  };
}""",
    "explanation": "Decorator factories encapsulate configuration in the top-level closure, returning a customized decorator that wraps functions with custom policies (like backoff, error filtering, and retry ceilings)."
}
