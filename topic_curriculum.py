"""
Curriculum definitions for standard JS topics to ensure instant, reliable, 100% accurate question suites.
"""

BINDING_AND_PARTIALS_QUESTIONS = [
    {
        "id": 1,
        "title": "Fixing Lost 'this' in Callbacks",
        "difficulty": "Fundamental",
        "concepts": ["Call site context", "Lost this", "Closure wrapper", "func.apply()"],
        "description": """
### Problem Statement
When an object method is passed as a callback (e.g., to `setTimeout` or an array method), its `this` reference to the original object is lost.

Write a utility function `bindMethod(obj, methodName)` that returns a wrapper function permanently bound to `obj`.

#### Requirements:
1. `bindMethod(obj, methodName)` should retrieve `obj[methodName]` and return a function.
2. When the returned function is called, it must execute `obj[methodName]` with `this` strictly pointing to `obj`.
3. Any arguments passed to the returned function must be forwarded to the original method.
4. The return value of the method must be returned by the wrapper.
""",
        "starter_code": """function bindMethod(obj, methodName) {
  // TODO: Return a function that calls obj[methodName] with obj as this
  return function(...args) {

  };
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "Passing `user.sayHi` as a standalone reference detaches it from `user`. You need `obj[methodName].apply(obj, args)` or `obj[methodName].call(obj, ...args)`."},
            {"tier": 2, "title": "Approach Strategy", "content": "Return a wrapper function `(...args) => obj[methodName].call(obj, ...args)` or use `function(...args) { return obj[methodName].apply(obj, args); }`."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction bindMethod(obj, methodName) {\n  return function(...args) {\n    return obj[methodName].apply(obj, args);\n  };\n}\n```"}
        ],
        "test_suite_js": """
await test('Preserves object context when called detached', () => {
    const user = {
        name: 'Alex',
        greet(greeting) {
            return `${greeting}, I am ${this.name}!`;
        }
    };
    const boundGreet = bindMethod(user, 'greet');
    
    // Simulate passing as callback
    function runner(cb) {
        return cb('Hello');
    }
    assertEqual(runner(boundGreet), 'Hello, I am Alex!');
});

await test('Forwards multiple arguments correctly', () => {
    const calc = {
        multiplier: 3,
        compute(a, b) {
            return (a + b) * this.multiplier;
        }
    };
    const boundCompute = bindMethod(calc, 'compute');
    assertEqual(boundCompute(4, 6), 30);
});
""",
        "solution_code": """function bindMethod(obj, methodName) {
  return function(...args) {
    return obj[methodName].apply(obj, args);
  };
}""",
        "explanation": "Extracting a method creates a bare function reference. Using `.apply(obj, args)` explicitly restores `this` to `obj` at invocation time."
    },
    {
        "id": 2,
        "title": "Custom Function.prototype.bind Implementation",
        "difficulty": "Fundamental",
        "concepts": ["myBind", "Bound arguments", "Context locking", "func.apply"],
        "description": """
### Problem Statement
Implement a custom version of `Function.prototype.bind` named `myBind(fn, context, ...boundArgs)`.

#### Requirements:
1. `myBind` takes a target function `fn`, a `context` to lock `this` to, and optional initial arguments (`...boundArgs`).
2. It returns a new function.
3. When the returned function is called with `...runtimeArgs`, it executes `fn` with `this` set to `context`, receiving combined arguments: `[...boundArgs, ...runtimeArgs]`.
4. Returns the result of `fn`.
*(Note: Do not use the built-in `.bind()` in your solution)*
""",
        "starter_code": """function myBind(fn, context, ...boundArgs) {
  // TODO: Implement custom bind with partial argument application
  
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "Combine `boundArgs` passed at bind-time with `runtimeArgs` passed at call-time."},
            {"tier": 2, "title": "Approach Strategy", "content": "Return `function(...runtimeArgs) { return fn.apply(context, [...boundArgs, ...runtimeArgs]); }`."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction myBind(fn, context, ...boundArgs) {\n  return function(...runtimeArgs) {\n    return fn.apply(context, boundArgs.concat(runtimeArgs));\n  };\n}\n```"}
        ],
        "test_suite_js": """
await test('Binds context and prepends arguments', () => {
    function greet(greeting, punctuation, name) {
        return `${greeting}, ${name}${punctuation} (${this.role})`;
    }
    const ctx = { role: 'Admin' };
    const bound = myBind(greet, ctx, 'Welcome', '!');
    assertEqual(bound('Sarah'), 'Welcome, Sarah! (Admin)');
});

await test('Works without initial bound arguments', () => {
    const person = { name: 'Elena' };
    function getName() {
        return this.name;
    }
    const bound = myBind(getName, person);
    assertEqual(bound(), 'Elena');
});
""",
        "solution_code": """function myBind(fn, context, ...boundArgs) {
  return function(...runtimeArgs) {
    return fn.apply(context, [...boundArgs, ...runtimeArgs]);
  };
}""",
        "explanation": "A bound function combines a fixed `this` reference with partially applied arguments at definition time, concatenating call-time arguments before invoking `.apply()`."
    },
    {
        "id": 3,
        "title": "Partial Application with Preserved Context",
        "difficulty": "Intermediate",
        "concepts": ["Partial application", "Call-site context", "Argument fixing", "func.call(this)"],
        "description": """
### Problem Statement
Create a `partial(fn, ...fixedArgs)` helper for partial function application.

Unlike `bind()`, which fixes both arguments AND the `this` context, a true general `partial` helper should **ONLY fix arguments** while **preserving whatever `this` context is present at the call site**.

#### Requirements:
1. `partial(fn, ...fixedArgs)` returns a function.
2. When the returned function is called (e.g. as a method on an object `obj.method(...)`), `this` inside `fn` MUST be the runtime `this` of the caller.
3. Arguments passed must be `[...fixedArgs, ...runtimeArgs]`.
""",
        "starter_code": """function partial(fn, ...fixedArgs) {
  // TODO: Fix arguments while preserving the runtime `this` from the call site
  
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "Do NOT use an arrow function for the returned function if you want dynamic `this`, or make sure to forward `this` explicitly via `.call(this, ...)`."},
            {"tier": 2, "title": "Approach Strategy", "content": "Use a standard `function(...runtimeArgs)` and invoke `fn.apply(this, [...fixedArgs, ...runtimeArgs])`."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction partial(fn, ...fixedArgs) {\n  return function(...runtimeArgs) {\n    return fn.apply(this, [...fixedArgs, ...runtimeArgs]);\n  };\n}\n```"}
        ],
        "test_suite_js": """
await test('Preserves caller context on object method call', () => {
    const user = {
        name: 'Jordan',
        say(time, phrase) {
            return `[${time}] ${this.name}: ${phrase}`;
        }
    };
    // Partially apply '10:00 AM' as time, but keep user as this
    user.sayMorning = partial(user.say, '10:00 AM');
    assertEqual(user.sayMorning('Good morning!'), '[10:00 AM] Jordan: Good morning!');
});

await test('Works standalone with regular functions', () => {
    function multiply(a, b, c) {
        return a * b * c;
    }
    const doubleAndScale = partial(multiply, 2);
    assertEqual(doubleAndScale(3, 4), 24);
});
""",
        "solution_code": """function partial(fn, ...fixedArgs) {
  return function(...runtimeArgs) {
    return fn.apply(this, [...fixedArgs, ...runtimeArgs]);
  };
}""",
        "explanation": "By returning a regular function, `this` is bound at invocation time. Forwarding `this` to `fn.apply(this, ...)` ensures that object methods retain their calling instance."
    },
    {
        "id": 4,
        "title": "Going Partial Without Context",
        "difficulty": "Intermediate",
        "concepts": ["Context stripping", "Partial without this", "Explicit undefined context", "Pure partial"],
        "description": """
### Problem Statement
Sometimes we want to create a partial function that explicitly **drops/ignores** any caller context, always executing `fn` in a pure context-free environment (`this = undefined`).

Write `partialWithoutContext(fn, ...fixedArgs)`.

#### Requirements:
1. Fixes `...fixedArgs` at the beginning of the argument list.
2. Even if the returned function is attached to an object and called as a method (e.g. `obj.calc(...)`), `fn` MUST be invoked with `this` set to `undefined`.
3. It must return the result of `fn`.
""",
        "starter_code": """function partialWithoutContext(fn, ...fixedArgs) {
  // TODO: Fix arguments and explicitly isolate fn from any caller `this`
  
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "How do you invoke a function so its `this` is explicitly `undefined` regardless of caller?"},
            {"tier": 2, "title": "Approach Strategy", "content": "Inside the returned wrapper, call `fn.apply(undefined, [...fixedArgs, ...runtimeArgs])`."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\\nfunction partialWithoutContext(fn, ...fixedArgs) {\\n  return function(...runtimeArgs) {\\n    return fn.apply(undefined, [...fixedArgs, ...runtimeArgs]);\\n  };\\n}\\n```"}
        ],
        "test_suite_js": """
await test('Explicitly removes context even when called on object', () => {
    'use strict';
    function inspect(a, b) {
        'use strict';
        return { context: this, sum: a + b };
    }
    const addFive = partialWithoutContext(inspect, 5);
    
    const obj = { name: 'Holder', addFive };
    const res = obj.addFive(10);
    assertEqual(res.sum, 15);
    assert(res.context === undefined, 'Context should be undefined');
});
""",
        "solution_code": """function partialWithoutContext(fn, ...fixedArgs) {
  return function(...runtimeArgs) {
    return fn.apply(undefined, [...fixedArgs, ...runtimeArgs]);
  };
}""",
        "explanation": "Passing `undefined` as the `thisArg` to `.apply()` ensures the target function cannot access or mutate the caller's object properties."
    },
    {
        "id": 5,
        "title": "Dynamic Auto-Currying with Context Support",
        "difficulty": "Intermediate",
        "concepts": ["Currying", "Arity tracking", "Recursive partials", "fn.length"],
        "description": """
### Problem Statement
Write a currying utility `curry(fn, arity)` that converts a function of N arguments into a chain of callable functions.

#### Requirements:
1. If `arity` is omitted, default to `fn.length`.
2. When called with fewer arguments than `arity`, return a new curried function waiting for the remaining arguments.
3. When enough arguments are collected, execute `fn` preserving any instance `this` context from the call site.
4. Support both single-arg chaining `curried(1)(2)(3)` and multi-arg calls `curried(1, 2)(3)`.
""",
        "starter_code": """function curry(fn, arity = fn.length) {
  // TODO: Return a curried version of fn supporting both partial and final execution
  
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "Accumulate arguments in a closure. Compare `args.length >= arity`."},
            {"tier": 2, "title": "Approach Strategy", "content": "If `args.length >= arity`, invoke `fn.apply(this, args)`. Otherwise, return a function that accepts `...nextArgs` and recurses."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\\nfunction curry(fn, arity = fn.length) {\\n  return function curried(...args) {\\n    if (args.length >= arity) return fn.apply(this, args);\\n    const savedThis = this;\\n    return function(...next) {\\n      const targetThis = (this !== undefined && typeof globalThis !== 'undefined' && this !== globalThis) ? this : savedThis;\\n      return curried.apply(targetThis, [...args, ...next]);\\n    };\\n  };\\n}\\n```"}
        ],
        "test_suite_js": """
await test('Curries 3-argument function step by step', () => {
    function volume(l, w, h) { return l * w * h; }
    const curriedVol = curry(volume);
    assertEqual(curriedVol(2)(3)(4), 24);
    assertEqual(curriedVol(2, 3)(4), 24);
    assertEqual(curriedVol(2)(3, 4), 24);
});

await test('Preserves context on final execution', () => {
    const multiplier = {
        factor: 10,
        calc(a, b) {
            return (a + b) * this.factor;
        }
    };
    multiplier.curriedCalc = curry(multiplier.calc);
    assertEqual(multiplier.curriedCalc(2)(3), 50);
});
""",
        "solution_code": """function curry(fn, arity = fn.length) {
  return function curried(...args) {
    if (args.length >= arity) {
      return fn.apply(this, args);
    }
    const savedThis = this;
    return function(...next) {
      const targetThis = (this !== undefined && typeof globalThis !== 'undefined' && this !== globalThis) ? this : savedThis;
      return curried.apply(targetThis, [...args, ...next]);
    };
  };
}""",
        "explanation": "Currying recursively accumulates arguments until the target arity is satisfied, forwarding the caller's `this` at the terminal invocation."
    },
    {
        "id": 6,
        "title": "Auto-Binding Object Methods (`bindAll`)",
        "difficulty": "Advanced",
        "concepts": ["Object method binding", "Destructuring safety", "In-place mutation", "Object.keys"],
        "description": """
### Problem Statement
Write a helper `bindAll(obj, ...methodNames)` that permanently binds methods on an object to that object.

#### Requirements:
1. If `methodNames` are provided as arguments, only bind those specific methods on `obj`.
2. If no `methodNames` are passed, bind ALL function properties found directly on `obj`.
3. Mutates `obj` by reassigning `obj[method] = obj[method].bind(obj)` for each target method.
4. Returns `obj` for method chaining.
""",
        "starter_code": """function bindAll(obj, ...methodNames) {
  // TODO: Bind specified methods (or all methods) to obj
  
  return obj;
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "Determine the list of method names: either `methodNames` or `Object.keys(obj).filter(k => typeof obj[k] === 'function')`."},
            {"tier": 2, "title": "Approach Strategy", "content": "Iterate over the targets and replace `obj[m] = obj[m].bind(obj)`."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction bindAll(obj, ...methodNames) {\n  const methods = methodNames.length > 0 \n    ? methodNames \n    : Object.keys(obj).filter(k => typeof obj[k] === 'function');\n  for (const m of methods) {\n    if (typeof obj[m] === 'function') {\n      obj[m] = obj[m].bind(obj);\n    }\n  }\n  return obj;\n}\n```"}
        ],
        "test_suite_js": """
await test('Binds all methods when none specified', () => {
    const controller = {
        name: 'Dashboard',
        render() { return `Rendering ${this.name}`; },
        close() { return `Closing ${this.name}`; }
    };
    bindAll(controller);
    
    const { render, close } = controller;
    assertEqual(render(), 'Rendering Dashboard');
    assertEqual(close(), 'Closing Dashboard');
});

await test('Binds only specified methods when provided', () => {
    const person = {
        name: 'Sam',
        sayName() { return this.name; },
        sayAge() { return this.age; },
        age: 25
    };
    bindAll(person, 'sayName');
    const { sayName, sayAge } = person;
    assertEqual(sayName(), 'Sam');
});
""",
        "solution_code": """function bindAll(obj, ...methodNames) {
  const methods = methodNames.length > 0
    ? methodNames
    : Object.keys(obj).filter(k => typeof obj[k] === 'function');
    
  for (const m of methods) {
    if (typeof obj[m] === 'function') {
      obj[m] = obj[m].bind(obj);
    }
  }
  return obj;
}""",
        "explanation": "`bindAll` safeguards against context loss when destructuring methods by locking each method to its host instance."
    },
    {
        "id": 7,
        "title": "Context-Forwarding Pipeline (`pipeWithContext`)",
        "difficulty": "Advanced",
        "concepts": ["Function composition", "Pipeline architecture", "Context preservation across steps"],
        "description": """
### Problem Statement
Write `pipeWithContext(...fns)` that composes multiple transformation functions into a pipeline.

#### Requirements:
1. `pipeWithContext(f1, f2, f3)` returns a function that passes initial input through `f1`, then its result to `f2`, then to `f3`.
2. **Context Requirement**: Every single function in the pipeline must be executed with the `this` context from the pipeline's call site!
3. The first function receives `...args`. Subsequent functions receive the single return value of the previous stage.
""",
        "starter_code": """function pipeWithContext(...fns) {
  // TODO: Return a pipeline function where all stages share the caller's `this`
  
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "Use `reduce` or a loop. Use `.apply(this, ...)` or `.call(this, ...)` at each step."},
            {"tier": 2, "title": "Approach Strategy", "content": "First function gets `fns[0].apply(this, args)`. Then iterate remaining functions using `fn.call(this, acc)`."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction pipeWithContext(...fns) {\n  return function(...args) {\n    if (fns.length === 0) return undefined;\n    let acc = fns[0].apply(this, args);\n    for (let i = 1; i < fns.length; i++) {\n      acc = fns[i].call(this, acc);\n    }\n    return acc;\n  };\n}\n```"}
        ],
        "test_suite_js": """
await test('Pipes transformations preserving object state access', () => {
    const formatter = {
        prefix: '>> ',
        suffix: ' <<',
        trim(s) { return s.trim(); },
        addPrefix(s) { return this.prefix + s; },
        addSuffix(s) { return s + this.suffix; }
    };
    
    formatter.format = pipeWithContext(
        formatter.trim,
        formatter.addPrefix,
        formatter.addSuffix
    );
    
    assertEqual(formatter.format('  hello world  '), '>> hello world <<');
});
""",
        "solution_code": """function pipeWithContext(...fns) {
  return function(...args) {
    if (fns.length === 0) return undefined;
    let result = fns[0].apply(this, args);
    for (let i = 1; i < fns.length; i++) {
      result = fns[i].call(this, result);
    }
    return result;
  };
}""",
        "explanation": "Standard pipelines often discard context. By invoking every step with `.call(this, ...)`, methods in the pipeline can read and write to instance state."
    },
    {
        "id": 8,
        "title": "Bug Hunt: The Broken Widget Timer",
        "difficulty": "Advanced",
        "concepts": ["Callback context loss", "Timer callbacks", "Arrow vs bound methods"],
        "description": """
### Problem Statement
A developer wrote a `TimerWidget` class that tracks ticks, but when `start()` is invoked, `this.count` is never incremented and errors are thrown because `this` becomes `global` or `undefined` inside `setInterval`.

Fix the implementation of `createTimerWidget(name)` so that:
1. `widget.start(intervalMs)` starts incrementing `this.count` by 1 every `intervalMs`.
2. `widget.stop()` clears the active interval.
3. `widget.getReport()` returns `"${this.name}: ${this.count} ticks"`.
4. Even if `widget.tick` or `widget.getReport` is passed as a detached callback, it must not fail.
""",
        "starter_code": """function createTimerWidget(name) {
  const widget = {
    name,
    count: 0,
    intervalId: null,
    tick() {
      this.count++;
    },
    start(intervalMs) {
      // BUG: this.tick loses this when invoked by setInterval
      this.intervalId = setInterval(this.tick, intervalMs);
    },
    stop() {
      clearInterval(this.intervalId);
    },
    getReport() {
      return `${this.name}: ${this.count} ticks`;
    }
  };
  return widget;
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "`setInterval(this.tick, intervalMs)` passes `this.tick` as a raw function pointer. When invoked by the runtime, `this` is no longer `widget`."},
            {"tier": 2, "title": "Approach Strategy", "content": "Bind `this.tick = this.tick.bind(this)` and `this.getReport = this.getReport.bind(this)`, or use arrow functions."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction createTimerWidget(name) {\n  const widget = {\n    name,\n    count: 0,\n    intervalId: null,\n    tick() { this.count++; },\n    start(intervalMs) { this.intervalId = setInterval(() => this.tick(), intervalMs); },\n    stop() { clearInterval(this.intervalId); },\n    getReport() { return `${this.name}: ${this.count} ticks`; }\n  };\n  widget.tick = widget.tick.bind(widget);\n  widget.getReport = widget.getReport.bind(widget);\n  return widget;\n}\n```"}
        ],
        "test_suite_js": """
await test('Timer correctly increments count and generates report', async () => {
    const w = createTimerWidget('CounterA');
    w.start(10);
    await new Promise(r => setTimeout(r, 45));
    w.stop();
    assert(w.count >= 2, `Count should be at least 2, got ${w.count}`);
    
    // Detached report call
    const reporter = w.getReport;
    assertEqual(reporter(), `CounterA: ${w.count} ticks`);
});
""",
        "solution_code": """function createTimerWidget(name) {
  const widget = {
    name,
    count: 0,
    intervalId: null,
    tick() {
      this.count++;
    },
    start(intervalMs) {
      this.intervalId = setInterval(this.tick, intervalMs);
    },
    stop() {
      clearInterval(this.intervalId);
    },
    getReport() {
      return `${this.name}: ${this.count} ticks`;
    }
  };
  widget.tick = widget.tick.bind(widget);
  widget.getReport = widget.getReport.bind(widget);
  return widget;
}""",
        "explanation": "Binding `tick` and `getReport` directly on the instance ensures that both timer callbacks and detached references always retain access to the instance properties."
    },
    {
        "id": 9,
        "title": "Safe Method Borrower with Argument Prepending",
        "difficulty": "Expert",
        "concepts": ["Method borrowing", "Generic function extraction", "Argument forwarding", "Polymorphism"],
        "description": """
### Problem Statement
Method borrowing allows an object to use a method belonging to another object or prototype (e.g. `Array.prototype.join`).

Write `borrowMethod(sourceProto, methodName, targetObj, ...fixedArgs)` that borrows a method and packages it for `targetObj`.

#### Requirements:
1. Returns a function bound to `targetObj`.
2. Any `fixedArgs` passed to `borrowMethod` are prepended before runtime arguments.
3. If `sourceProto[methodName]` does not exist or is not a function, throw a `TypeError`.
4. The borrowed method executes with `this === targetObj`.
""",
        "starter_code": """function borrowMethod(sourceProto, methodName, targetObj, ...fixedArgs) {
  // TODO: Safely borrow method from sourceProto and bind to targetObj with fixedArgs
  
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "Check `typeof sourceProto[methodName] !== 'function'` first. Then return a function calling `sourceProto[methodName].apply(targetObj, ...)`."},
            {"tier": 2, "title": "Approach Strategy", "content": "Validate the method, then return `(...runtimeArgs) => method.apply(targetObj, [...fixedArgs, ...runtimeArgs])`."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction borrowMethod(sourceProto, methodName, targetObj, ...fixedArgs) {\n  const fn = sourceProto ? sourceProto[methodName] : undefined;\n  if (typeof fn !== 'function') {\n    throw new TypeError(`Method ${methodName} not found`);\n  }\n  return function(...runtime) {\n    return fn.apply(targetObj, [...fixedArgs, ...runtime]);\n  };\n}\n```"}
        ],
        "test_suite_js": """
await test('Borrows Array.prototype method onto array-like object', () => {
    const arrayLike = { 0: 'a', 1: 'b', 2: 'c', length: 3 };
    const customJoin = borrowMethod(Array.prototype, 'join', arrayLike, '-');
    assertEqual(customJoin(), 'a-b-c');
});

await test('Throws TypeError on non-existent method', () => {
    let threw = false;
    try {
        borrowMethod({}, 'nonExistent', {});
    } catch (e) {
        threw = (e instanceof TypeError);
    }
    assert(threw, 'Expected TypeError for missing method');
});
""",
        "solution_code": """function borrowMethod(sourceProto, methodName, targetObj, ...fixedArgs) {
  const method = sourceProto ? sourceProto[methodName] : undefined;
  if (typeof method !== 'function') {
    throw new TypeError(`Method '${methodName}' is not a function`);
  }
  return function(...runtimeArgs) {
    return method.apply(targetObj, [...fixedArgs, ...runtimeArgs]);
  };
}""",
        "explanation": "Method borrowing extracts generic methods and pairs them with arbitrary targets and pre-configured arguments using `.apply(targetObj, combinedArgs)`."
    },
    {
        "id": 10,
        "title": "Diagnostic: Dynamic Context Switchboard",
        "difficulty": "Expert",
        "concepts": ["Dynamic context switching", "Handler registry", "Partial argument injection", "Unbinding"],
        "description": """
### Problem Statement
Build a `createSwitchboard()` registry that manages event handlers with dynamic context reassignment and partial argument binding.

#### Requirements:
1. `switchboard.register(event, handler, defaultContext, ...defaultArgs)`:
   - Registers a handler function for an event name.
2. `switchboard.trigger(event, overrideContext, ...triggerArgs)`:
   - Invokes all registered handlers for `event`.
   - Uses `overrideContext` as `this` if provided; otherwise falls back to `defaultContext` registered with the handler.
   - Arguments received by handler must be `[...defaultArgs, ...triggerArgs]`.
   - Returns an array containing the results of each handler executed in order.
3. `switchboard.unbind(event)`:
   - Removes all handlers for `event`.
""",
        "starter_code": """function createSwitchboard() {
  const events = new Map();

  return {
    register(event, handler, defaultContext, ...defaultArgs) {
      // TODO: Register handler with context and partial arguments
      
    },
    trigger(event, overrideContext, ...triggerArgs) {
      // TODO: Execute handlers with overrideContext || defaultContext
      
    },
    unbind(event) {
      // TODO: Clear handlers for event
      
    }
  };
}""",
        "hints": [
            {"tier": 1, "title": "Conceptual Nudge", "content": "Store an array of `{ handler, defaultContext, defaultArgs }` objects per event in the Map."},
            {"tier": 2, "title": "Approach Strategy", "content": "When triggering, loop through items. Compute `ctx = (overrideContext !== undefined && overrideContext !== null) ? overrideContext : item.defaultContext`. Invoke `item.handler.apply(ctx, [...item.defaultArgs, ...triggerArgs])`."},
            {"tier": 3, "title": "Code Skeleton", "content": "```javascript\nfunction createSwitchboard() {\n  const events = new Map();\n  return {\n    register(event, handler, defaultContext, ...defaultArgs) {\n      if (!events.has(event)) events.set(event, []);\n      events.get(event).push({ handler, defaultContext, defaultArgs });\n    },\n    trigger(event, overrideContext, ...triggerArgs) {\n      const handlers = events.get(event) || [];\n      return handlers.map(h => {\n        const ctx = overrideContext !== undefined ? overrideContext : h.defaultContext;\n        return h.handler.apply(ctx, [...h.defaultArgs, ...triggerArgs]);\n      });\n    },\n    unbind(event) {\n      events.delete(event);\n    }\n  };\n}\n```"}
        ],
        "test_suite_js": """
await test('Executes handlers with default context and partial args', () => {
    const sb = createSwitchboard();
    const serviceA = { id: 'A', log(level, msg) { return `[${this.id}] ${level}: ${msg}`; } };
    
    sb.register('alert', serviceA.log, serviceA, 'WARN');
    const results = sb.trigger('alert', null, 'Disk space low');
    assertEqual(results, ['[A] WARN: Disk space low']);
});

await test('Allows overriding context on trigger', () => {
    const sb = createSwitchboard();
    function format(tag) { return `${tag} by ${this.user}`; }
    
    sb.register('action', format, { user: 'Default' }, '#audit');
    const results = sb.trigger('action', { user: 'Admin' });
    assertEqual(results, ['#audit by Admin']);
});

await test('Unbind clears handlers', () => {
    const sb = createSwitchboard();
    sb.register('ping', () => 'pong', null);
    assertEqual(sb.trigger('ping'), ['pong']);
    sb.unbind('ping');
    assertEqual(sb.trigger('ping'), []);
});
""",
        "solution_code": """function createSwitchboard() {
  const events = new Map();

  return {
    register(event, handler, defaultContext, ...defaultArgs) {
      if (!events.has(event)) {
        events.set(event, []);
      }
      events.get(event).push({ handler, defaultContext, defaultArgs });
    },
    trigger(event, overrideContext, ...triggerArgs) {
      const handlers = events.get(event) || [];
      return handlers.map(h => {
        const ctx = (overrideContext !== null && overrideContext !== undefined)
          ? overrideContext
          : h.defaultContext;
        return h.handler.apply(ctx, [...h.defaultArgs, ...triggerArgs]);
      });
    },
    unbind(event) {
      events.delete(event);
    }
  };
}""",
        "explanation": "A context switchboard demonstrates mastery of dynamic context resolution: handlers hold default contexts and partial arguments that can be dynamically overridden at trigger time."
    }
]
