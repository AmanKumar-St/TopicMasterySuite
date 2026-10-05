"""
Question 5: Decorator Composition Order
Focus: Function composition, onion-skin execution flow, wrapper nesting, context propagation through chains.
"""

Q5 = {
    "id": 5,
    "title": "Decorator Composition Engine",
    "difficulty": "Intermediate",
    "concepts": ["Function composition", "Decorator chaining", "Pipeline execution order", "Context propagation"],
    "description": """
### Problem Statement
Write a higher-order function `composeDecorators(...decorators)` that takes any number of decorators and returns a single combined decorator.

#### Requirements:
1. When the combined decorator wraps a function `fn` (`const decorated = composeDecorators(d1, d2, d3)(fn)`), it must apply them such that `d1` is the outermost wrapper, followed by `d2`, followed by `d3` (i.e. `d1(d2(d3(fn)))`).
2. When the final decorated function is invoked, the execution order must flow through `d1` $\rightarrow$ `d2` $\rightarrow$ `d3` $\rightarrow$ `fn`, and then unwind return values back up through `d3` $\rightarrow$ `d2` $\rightarrow$ `d1`.
3. The `this` context and all arguments must be transparently preserved across the entire composition chain.
4. If no decorators are passed (`composeDecorators()`), it should return the original function unmodified.
""",
    "starter_code": """function composeDecorators(...decorators) {
  return function(fn) {
    // TODO: Apply decorators in right-to-left reduction so the first decorator is outermost
    
  };
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "To make `d1` outermost and execute first, `d1` must wrap the result of `d2`, which wraps `d3(fn)`. Think about `Array.prototype.reduceRight`."
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "Use `decorators.reduceRight((wrappedFn, decorator) => decorator(wrappedFn), fn)` to fold the decorators from innermost to outermost."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function composeDecorators(...decorators) {
  return function(fn) {
    return decorators.reduceRight((acc, dec) => dec(acc), fn);
  };
}
```"""
        }
    ],
    "test_suite_js": """
await test('Composes decorators in correct outermost-first order', () => {
    const trace = [];

    const logger1 = (fn) => function(...args) {
        trace.push('enter-1');
        const res = fn.apply(this, args);
        trace.push('exit-1');
        return res;
    };

    const logger2 = (fn) => function(...args) {
        trace.push('enter-2');
        const res = fn.apply(this, args);
        trace.push('exit-2');
        return res;
    };

    const core = function(x) {
        trace.push('core:' + x);
        return x * 2;
    };

    const decorated = composeDecorators(logger1, logger2)(core);
    const result = decorated(5);

    assertEqual(result, 10, 'Computes correct result');
    assertEqual(trace, ['enter-1', 'enter-2', 'core:5', 'exit-2', 'exit-1'], 'Exact onion-skin execution flow');
});

await test('Maintains object context across multiple decorators', () => {
    const doubleResult = (fn) => function(...args) {
        return fn.apply(this, args) * 2;
    };
    const addOffset = (fn) => function(...args) {
        return fn.apply(this, args) + this.offset;
    };

    const calculator = {
        offset: 5,
        base(n) {
            return n + 1;
        }
    };

    // d1(d2(base)) -> doubleResult(addOffset(base))
    // (5 + 1) + 5 = 11 -> 11 * 2 = 22
    calculator.base = composeDecorators(doubleResult, addOffset)(calculator.base);
    assertEqual(calculator.base(5), 22, 'Context is preserved through nested decorators');
});
""",
    "solution_code": """function composeDecorators(...decorators) {
  return function(fn) {
    return decorators.reduceRight((acc, dec) => dec(acc), fn);
  };
}""",
    "explanation": "`reduceRight` starts with `fn` as the initial accumulator and progressively wraps it with the rightmost decorator through to the leftmost. The leftmost decorator becomes the outermost wrapper."
}
