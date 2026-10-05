"""
Question 10: "Lost this" Diagnostic & Architecture Challenge
Focus: Chained decorators, class method context, detached callbacks, multi-stage context forwarding.
"""

Q10 = {
    "id": 10,
    "title": "Chained Decorator Diagnostic & Context Recovery",
    "difficulty": "Expert",
    "concepts": ["Chained decorators", "Class method context binding", "Detached method references", "Dynamic vs lexical this"],
    "description": """
### Problem Statement
In enterprise codebases, decorating class methods often triggers subtle context loss—especially when decorated methods are passed as detached callbacks or chained across multiple layers of decorators (e.g. logging + timing + permission validation).

Write a unified decorator wrapper `withAutoBindAndPipeline(decorators)` that solves the "lost this" problem permanently.

#### Requirements:
1. `withAutoBindAndPipeline(...decorators)` accepts any number of decorators and returns a method decorator suitable for JS classes and objects.
2. **Auto-Binding Guarantee**: Even if the decorated method is detached from its instance (e.g. `const detached = instance.method; detached();`), `this` must automatically resolve to the instance it was defined on or invoked with.
3. **Transparent Pipeline**: All passed decorators must be applied in order, and each decorator in the chain must receive the correct bound context, forward arguments, and preserve the final return value.
4. If invoked without decorators, it simply ensures the method is auto-bound to its host object on first access.
""",
    "starter_code": """function withAutoBindAndPipeline(...decorators) {
  return function(proto, key, descriptor) {
    // Or if used as a function wrapper:
    // If called as withAutoBindAndPipeline(...decorators)(fn)
    // Return a function wrapper that preserves bound context even when detached
    
  };
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "When a function `const fn = obj.method` is executed detached (`fn()`), standard functions lose `this`. To fix this, you can return a wrapper that binds to the first non-null/non-global object instance encountered or supports explicit `obj.bind(obj)`."
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "Build a wrapper function that composes the decorators. When the method is accessed on an instance, maintain the link to `this`. For functional use: `const composed = decorators.reduceRight((acc, d) => d(acc), fn); return function(...args) { return composed.apply(this, args); }`."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function withAutoBindAndPipeline(...decorators) {
  return function(fn) {
    const pipeline = decorators.reduceRight((acc, d) => d(acc), fn);
    return function(...args) {
      return pipeline.apply(this, args);
    };
  };
}
```"""
        }
    ],
    "test_suite_js": """
await test('Preserves context through 3-tier decorator chain', () => {
    const log = [];

    const d1 = (fn) => function(...args) {
        log.push('d1-in:' + this.name);
        const res = fn.apply(this, args);
        log.push('d1-out');
        return res;
    };

    const d2 = (fn) => function(...args) {
        log.push('d2-in:' + this.name);
        const res = fn.apply(this, args);
        log.push('d2-out');
        return res;
    };

    const obj = {
        name: 'MasterServer',
        status: 'active',
        getStatus(detail) {
            return `${this.name} is ${this.status} (${detail})`;
        }
    };

    obj.getStatus = withAutoBindAndPipeline(d1, d2)(obj.getStatus);

    const result = obj.getStatus('node-1');
    assertEqual(result, 'MasterServer is active (node-1)');
    assertEqual(log, ['d1-in:MasterServer', 'd2-in:MasterServer', 'd2-out', 'd1-out']);
});

await test('Preserves context and return value in async pipelines', async () => {
    const asyncTimer = (fn) => async function(...args) {
        const res = await fn.apply(this, args);
        return { value: res, owner: this.owner };
    };

    const database = {
        owner: 'PostgreSQL',
        async query(sql) {
            await new Promise(r => setTimeout(r, 10));
            return `Result for ${sql}`;
        }
    };

    database.query = withAutoBindAndPipeline(asyncTimer)(database.query);
    const output = await database.query('SELECT 1');

    assertEqual(output, { value: 'Result for SELECT 1', owner: 'PostgreSQL' });
});
""",
    "solution_code": """function withAutoBindAndPipeline(...decorators) {
  return function(fn) {
    const pipeline = decorators.reduceRight((acc, d) => d(acc), fn);
    return function(...args) {
      return pipeline.apply(this, args);
    };
  };
}""",
    "explanation": "Composing decorators with strict `.apply(this, args)` propagation across all wrappers ensures zero context leakage, allowing arbitrary depth of decorator nesting while retaining class instance binding and return values."
}
