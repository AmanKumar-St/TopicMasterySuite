"""
Question 3: Method Borrowing Deep-Dive
Focus: Array.prototype borrowing, `call`/`apply` on array-like objects, handling non-array iterables.
"""

Q3 = {
    "id": 3,
    "title": "Method Borrowing Deep-Dive",
    "difficulty": "Fundamental",
    "concepts": ["Array method borrowing", "Array.prototype.slice.call", "Array-like objects", "Object.prototype.hasOwnProperty"],
    "description": """
### Problem Statement
Write a utility function `transformArrayLike(arrayLike, mapFn, filterFn)` that performs functional operations on array-like objects (e.g. `arguments`, DOM NodeLists, or custom objects with numeric keys and a `length` property) **without converting the entire object to a native array first**.

#### Requirements:
1. Borrow `Array.prototype.filter` and `Array.prototype.map` using `.call()` to filter and then map elements directly over `arrayLike`.
2. If `filterFn` is provided, filter the elements using `[].filter.call(arrayLike, filterFn)`. If omitted, all elements pass.
3. If `mapFn` is provided, transform the filtered elements using `[].map.call(filtered, mapFn)`. If omitted, elements remain unchanged.
4. Return a native Array containing the final transformed elements.
5. Must handle sparse objects or custom objects like `{ 0: 'a', 1: 'b', length: 2 }` correctly.
""",
    "starter_code": """function transformArrayLike(arrayLike, mapFn, filterFn) {
  // TODO: Use Array method borrowing with .call() to filter and map over arrayLike
  
}""",
    "hints": [
        {
            "tier": 1,
            "title": "Conceptual Nudge",
            "content": "Native array methods like `Array.prototype.filter` only require the `this` value to have numeric indices and a `.length` property. You can invoke them on anything array-like via `Array.prototype.filter.call(target, fn)`."
        },
        {
            "tier": 2,
            "title": "Approach Strategy",
            "content": "First, if `filterFn` is provided, call `Array.prototype.filter.call(arrayLike, filterFn)`. Next, on the filtered result, invoke `Array.prototype.map.call(...)` if `mapFn` is provided."
        },
        {
            "tier": 3,
            "title": "Code Skeleton",
            "content": """```javascript
function transformArrayLike(arrayLike, mapFn, filterFn) {
  let result = filterFn 
    ? Array.prototype.filter.call(arrayLike, filterFn)
    : Array.prototype.slice.call(arrayLike);

  if (mapFn) {
    result = Array.prototype.map.call(result, mapFn);
  }
  return result;
}
```"""
        }
    ],
    "test_suite_js": """
await test('Transforms pseudo-array objects', () => {
    const fakeArray = { 0: 10, 1: 25, 2: 30, 3: 5, length: 4 };
    const filteredAndDoubled = transformArrayLike(
        fakeArray,
        x => x * 2,
        x => x > 15
    );
    assertEqual(filteredAndDoubled, [50, 60], 'Filters > 15 and doubles');
});

await test('Works on arguments object within a function', () => {
    function processArgs() {
        return transformArrayLike(arguments, str => str.toUpperCase(), str => str.startsWith('a'));
    }
    const res = processArgs('apple', 'banana', 'avocado', 'cherry');
    assertEqual(res, ['APPLE', 'AVOCADO']);
});

await test('Handles missing filter or map callbacks', () => {
    const obj = { 0: 'x', 1: 'y', length: 2 };
    const cloned = transformArrayLike(obj);
    assertEqual(cloned, ['x', 'y']);
});
""",
    "solution_code": """function transformArrayLike(arrayLike, mapFn, filterFn) {
  let result = filterFn 
    ? Array.prototype.filter.call(arrayLike, filterFn)
    : Array.prototype.slice.call(arrayLike);

  if (mapFn) {
    result = Array.prototype.map.call(result, mapFn);
  }
  return result;
}""",
    "explanation": "Method borrowing works because the ECMAScript specification defines many Array methods generically: they only inspect the `length` property and integer-keyed properties on whatever object is provided as `this`."
}
