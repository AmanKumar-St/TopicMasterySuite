"""
Question 6: Preserving Function Properties & Descriptors
Focus: Function metadata preservation, Object.getOwnPropertyDescriptors, Object.defineProperties, Proxies.
"""

Q6 = {
    "id": 6,
    "title": "Preserving Function Properties & Metadata",
    "difficulty": "Advanced",
    "concepts": ["Object.getOwnPropertyDescriptors", "Object.defineProperties", "Function.name and length preservation", "Proxy trapping"],
    "description": """
### Problem Statement
When functions are wrapped by decorators, custom properties (like `.description`, `.roles`, or default values) and intrinsic properties (`.length`, `.name`) are typically lost.

Implement a utility `wrapWithMetadata(targetFunc, wrapperFunc)` that wraps `targetFunc` with `wrapperFunc` while **fully preserving all own properties and descriptors** of `targetFunc` on the wrapper.

#### Requirements:
1. When the decorated function is called, it must execute `wrapperFunc` (which forwards to `targetFunc`).
2. All custom own properties on `targetFunc` (enumerable and non-enumerable, including Symbols) must exist on `wrapperFunc` with identical property descriptors (`writable`, `enumerable`, `configurable`).
3. Intrinsic properties like `.name` and `.length` should match `targetFunc`'s original name and arity.
4. Returns the fully configured wrapper function.
""",
    "starter_code": """function wrapWithMetadata(targetFunc, wrapperFunc) {
  // TODO: Clone all property descriptors from targetFunc onto wrapperFunc
  
  return wrapperFunc;
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "A simple `Object.assign` misses non-enumerable properties and symbol properties, and does not preserve custom getters/setters or descriptor flags. `Object.getOwnPropertyDescriptors` retrieves all own descriptors."
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "Retrieve all descriptors with `Object.getOwnPropertyDescriptors(targetFunc)` and define them onto `wrapperFunc` using `Object.defineProperties(wrapperFunc, descriptors)`. Note that some standard descriptors on functions may have `configurable: true` which allows redefinition."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function wrapWithMetadata(targetFunc, wrapperFunc) {
  const descriptors = Object.getOwnPropertyDescriptors(targetFunc);
  
  for (const [prop, descriptor] of Object.entries(descriptors)) {
    try {
      Object.defineProperty(wrapperFunc, prop, descriptor);
    } catch (e) {
      // Ignore non-configurable native properties if cannot be overwritten
    }
  }
  
  return wrapperFunc;
}
```"""
        }
    ],
    "test_suite_js": """
await test('Preserves custom static properties and function length', () => {
    function greet(first, last, title) {
        return `Hello ${title} ${first} ${last}`;
    }
    greet.role = 'admin';
    greet.version = '1.2.0';
    Object.defineProperty(greet, 'hiddenId', {
        value: 'SECRET-999',
        enumerable: false,
        writable: false
    });

    const wrapper = function(...args) {
        return greet.apply(this, args);
    };

    const enhanced = wrapWithMetadata(greet, wrapper);

    assertEqual(enhanced.length, 3, 'Preserved function arity (.length)');
    assertEqual(enhanced.name, 'greet', 'Preserved function name');
    assertEqual(enhanced.role, 'admin', 'Preserved custom property');
    assertEqual(enhanced.version, '1.2.0');
    assertEqual(enhanced.hiddenId, 'SECRET-999', 'Preserved non-enumerable descriptor property');
});

await test('Preserves execution behavior', () => {
    function square(n) { return n * n; }
    square.category = 'math';

    const wrapped = wrapWithMetadata(square, function(n) {
        return square.call(this, n) + 1;
    });

    assertEqual(wrapped(4), 17, 'Wrapper logic runs correctly');
    assertEqual(wrapped.category, 'math', 'Property preserved');
});
""",
    "solution_code": """function wrapWithMetadata(targetFunc, wrapperFunc) {
  const descriptors = Object.getOwnPropertyDescriptors(targetFunc);
  
  for (const [prop, descriptor] of Object.entries(descriptors)) {
    try {
      Object.defineProperty(wrapperFunc, prop, descriptor);
    } catch (e) {
      // Ignore native non-configurable properties if runtime restricts
    }
  }
  
  return wrapperFunc;
}""",
    "explanation": "`Object.getOwnPropertyDescriptors` inspects all properties (enumerable, non-enumerable, symbols) and their descriptor configs (`get`, `set`, `writable`, `configurable`, `enumerable`). Copying these descriptors ensures complete transparency for decorators."
}
