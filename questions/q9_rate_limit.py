"""
Question 9: Rate-Limited & Concurrency-Controlled Decorator
Focus: Async concurrency control, Promise queueing, task scheduling, preserving context in queued callbacks.
"""

Q9 = {
    "id": 9,
    "title": "Async Concurrency Limiter Decorator",
    "difficulty": "Expert",
    "concepts": ["Async task queue", "Concurrency limiting", "Promise management", "Context retention in queue"],
    "description": """
### Problem Statement
In high-throughput systems, hitting external APIs requires strict concurrency control.

Write a decorator `concurrencyLimit(func, maxConcurrent)` that limits the number of simultaneously active asynchronous invocations of `func` to `maxConcurrent`.

#### Requirements:
1. If the number of running invocations is less than `maxConcurrent`, immediately invoke `func` with the provided context and arguments.
2. If the limit is reached, any additional invocations must be queued and wait until a running invocation finishes (resolves or rejects).
3. Invocations in the queue must be processed in **FIFO (First-In, First-Out)** order as slots open up.
4. Each caller receives a Promise that resolves or rejects with the exact outcome of their specific execution.
5. The decorator must preserve the runtime `this` context for all queued calls.
""",
    "starter_code": """function concurrencyLimit(func, maxConcurrent) {
  let activeCount = 0;
  const queue = [];

  // Helper to run next item in queue
  function runNext() {
    // TODO: Dequeue and execute next task if activeCount < maxConcurrent
  }

  return function(...args) {
    // TODO: Return a Promise that resolves when this specific invocation completes
    
  };
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "Return a new `Promise((resolve, reject) => { ... })` for every invocation. Store the `resolve`, `reject`, `context (this)`, and `args` in the queue."
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "In the wrapper, push `{ context: this, args, resolve, reject }` into `queue`. Then call `runNext()`. In `runNext()`, while `activeCount < maxConcurrent && queue.length > 0`, take an item, increment `activeCount`, run `func.apply(context, args)`, and in `finally`, decrement `activeCount` and call `runNext()`."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function concurrencyLimit(func, maxConcurrent) {
  let activeCount = 0;
  const queue = [];

  function runNext() {
    if (activeCount >= maxConcurrent || queue.length === 0) return;
    const { context, args, resolve, reject } = queue.shift();
    activeCount++;

    Promise.resolve()
      .then(() => func.apply(context, args))
      .then(resolve, reject)
      .finally(() => {
        activeCount--;
        runNext();
      });
  }

  return function(...args) {
    return new Promise((resolve, reject) => {
      queue.push({ context: this, args, resolve, reject });
      runNext();
    });
  };
}
```"""
        }
    ],
    "test_suite_js": """
await test('Enforces maximum concurrent executions', async () => {
    let active = 0;
    let maxObserved = 0;

    const asyncTask = async (id, duration) => {
        active++;
        maxObserved = Math.max(maxObserved, active);
        await new Promise(r => setTimeout(r, duration));
        active--;
        return `done-${id}`;
    };

    const limited = concurrencyLimit(asyncTask, 2);

    const promises = [
        limited(1, 40),
        limited(2, 40),
        limited(3, 40),
        limited(4, 40)
    ];

    const results = await Promise.all(promises);
    assertEqual(results, ['done-1', 'done-2', 'done-3', 'done-4'], 'All tasks completed successfully');
    assertEqual(maxObserved <= 2, true, `Max concurrent tasks was ${maxObserved}, which is <= 2`);
});

await test('Preserves this context for queued calls', async () => {
    const service = {
        prefix: 'ID:',
        async fetchItem(id) {
            await new Promise(r => setTimeout(r, 20));
            return this.prefix + id;
        }
    };

    service.fetchItem = concurrencyLimit(service.fetchItem, 1);

    const [a, b] = await Promise.all([
        service.fetchItem(100),
        service.fetchItem(200)
    ]);

    assertEqual(a, 'ID:100');
    assertEqual(b, 'ID:200');
});
""",
    "solution_code": """function concurrencyLimit(func, maxConcurrent) {
  let activeCount = 0;
  const queue = [];

  function runNext() {
    if (activeCount >= maxConcurrent || queue.length === 0) {
      return;
    }

    const { context, args, resolve, reject } = queue.shift();
    activeCount++;

    Promise.resolve()
      .then(() => func.apply(context, args))
      .then(resolve, reject)
      .finally(() => {
        activeCount--;
        runNext();
      });
  }

  return function(...args) {
    return new Promise((resolve, reject) => {
      queue.push({ context: this, args, resolve, reject });
      runNext();
    });
  };
}""",
    "explanation": "By decoupling the caller's Promise resolution from immediate execution, a FIFO queue can control execution pacing while preserving both the return channel (resolve/reject) and the original `this` context."
}
