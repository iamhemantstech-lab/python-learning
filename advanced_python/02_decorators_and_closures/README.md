# Topic 2: Decorators & Closures in Python

This module covers the internal mechanics of Python closures, parameterized decorators, metadata preservation, and stateful class decorators.

---

## 1. What is a Closure in CPython?

A **Closure** is a function that remembers and retains access to variables from its enclosing lexical scope even after the outer function has returned and exited the call stack.

### How CPython Implements It:
When a nested function accesses an outer variable:
1. Python marks that variable as a **Free Variable** (`func.__code__.co_freevars`).
2. Instead of storing it on the temporary call stack, Python allocates a **`cell` object on the Heap**.
3. The nested function receives a reference to this cell in its internal **`func.__closure__`** attribute.

📁 **Code:** [01_closures_and_lexical_scope.py](file:///c:/Users/ADMIN/Documents/hemant-python/advanced_python/02_decorators_and_closures/01_closures_and_lexical_scope.py)

---

## 2. Parameterized Decorators & The 3-Layer Pattern

A standard decorator takes only one argument: the target function.  
When a decorator takes arguments (e.g. `@retry(max_attempts=3, backoff=2.0)`), you must construct **3 nested function layers**:

```
 ┌────────────────────────────────────────────────────────┐
 │ LAYER 1: The Decorator Factory                         │
 │ def retry(max_attempts=3, backoff=2.0):                │
 └──────────────────────────┬─────────────────────────────┘
                            │ Returns Decorator
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ LAYER 2: The Decorator Function                        │
 │ def decorator(func):                                   │
 └──────────────────────────┬─────────────────────────────┘
                            │ Returns Wrapper
                            ▼
 ┌────────────────────────────────────────────────────────┐
 │ LAYER 3: The Call Interceptor                          │
 │ @functools.wraps(func)                                 │
 │ def wrapper(*args, **kwargs):                          │
 │     # Retry logic & error handling here                │
 └────────────────────────────────────────────────────────┘
```

### Why `@functools.wraps` is Mandatory in Production:
When you wrap a function, the wrapper takes over. Without `@functools.wraps(func)`:
* `func.__name__` becomes `"wrapper"`.
* `func.__doc__` becomes `None`.
* `inspect.signature(func)` loses original parameter names.
* **FastAPI consequence:** FastAPI uses inspection to build Swagger docs and inject dependencies; without `@wraps`, Swagger docs break and dependency injection fails!

📁 **Code:** [02_parameterized_decorators.py](file:///c:/Users/ADMIN/Documents/hemant-python/advanced_python/02_decorators_and_closures/02_parameterized_decorators.py)

---

## 3. Class-Based Decorators with `__call__`

In Python, any object implementing the magic method **`__call__`** is a callable object.

### When to use a Class-Based Decorator:
* When the decorator must **track persistent state** (e.g., cache hits/misses, call counters, circuit breakers).
* When you want to attach **utility methods** directly onto the decorated function (e.g., `func.clear_cache()`, `func.get_stats()`).

📁 **Code:** [03_class_based_decorators.py](file:///c:/Users/ADMIN/Documents/hemant-python/advanced_python/02_decorators_and_closures/03_class_based_decorators.py)

---

## 4. Top Interview Questions & Model Answers

### Q1: What is the difference between a function attribute and a closure variable?
* **Function Attribute (`func.count = 1`):** Publicly accessible and mutable from outside the function by anyone (`print(func.count)`).
* **Closure Variable (`__closure__`):** Encapsulated within the lexical scope. It provides true data hiding/privacy, accessible only through the inner function logic.

### Q2: What is the `nonlocal` keyword and when must you use it in closures?
In Python, assigning to a variable inside an inner function (`x = 5`) implicitly creates a *new local variable*.  
To modify an existing variable from the enclosing scope without creating a new local variable, you must explicitly declare `nonlocal x`.

### Q3: What is the exact execution order when chaining multiple decorators?
```python
@decorator_a
@decorator_b
def my_func():
    pass
```
* **Decoration time (bottom to top):** `my_func = decorator_a(decorator_b(my_func))`
* **Execution time (top to bottom):** `decorator_a` runs first, wraps `decorator_b`, which wraps `my_func`.

### Q4: How does `@functools.wraps` actually work under the hood?
It calls `functools.update_wrapper()`, which copies internal attributes from the original function to the wrapper:
* `__name__` (function name)
* `__doc__` (docstring)
* `__module__` (originating module)
* `__annotations__` (type hints)
* Sets `__wrapped__` pointing to the raw original function.
