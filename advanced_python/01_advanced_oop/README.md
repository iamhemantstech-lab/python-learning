# Topic 1: Advanced Object-Oriented Programming (OOP) in Python

This module covers advanced Python OOP patterns required for senior backend engineering and technical interviews.

---

## 1. Abstract Base Classes (ABC) & Composition

### The Core Concept:
* **`abc.ABC` + `@abstractmethod`**: Used to define strict interfaces (contracts) in Python. If a child class fails to implement any abstract method, Python raises a `TypeError` at instantiation time.
* **Composition over Inheritance ("Has-A" vs "Is-A")**:
  * *Bad (Inheritance):* `class UserService(EmailNotifier)` $\rightarrow$ Tight coupling. Cannot switch to SMS or Slack without rewriting the class hierarchy.
  * *Good (Composition):* `class UserService:` takes a `notifier: BaseNotifier` as an injected dependency. The notification provider can be swapped at runtime without changing a single line of business logic.

📁 **Code:** [01_abc_and_composition.py](file:///c:/Users/ADMIN/Documents/hemant-python/advanced_python/01_advanced_oop/01_abc_and_composition.py)

---

## 2. The Diamond Problem & Method Resolution Order (MRO)

### The Misconception:
> *"Does `super()` simply call the direct parent class?"*  
> **NO!** In Python, `super()` calls the **next class in the Method Resolution Order (MRO) list**, calculated using Python's **C3 Linearization** algorithm.

### The Diamond Structure:
```
           [BaseService]
             /        \
    [AuditMixin]    [MetricsMixin]
             \        /
         [PaymentService]
```

### The Computed MRO:
```python
PaymentService -> AuditMixin -> MetricsMixin -> BaseService -> object
```

### Why This Matters:
When `AuditMixin` calls `super().execute()`, it does **not** call `BaseService`! It dynamically calls `MetricsMixin`. This is called **Cooperative Multiple Inheritance**.

📁 **Code:** [02_mro_and_super.py](file:///c:/Users/ADMIN/Documents/hemant-python/advanced_python/01_advanced_oop/02_mro_and_super.py)

---

## 3. Memory Optimization: `__slots__` vs `__dict__`

### How CPython Stores Attributes:
* **Standard Class:** Every object holds a hidden dictionary (`self.__dict__`). Because Python dictionaries are dynamic hash tables, they consume substantial memory overhead.
* **`__slots__` Class:** Python removes `__dict__` and replaces it with a fixed-size C array of pointers.

### Benchmark Results (400,000 objects in RAM):
* Standard Class: **67.2 MB**
* `__slots__` Class: **51.9 MB**
* **Instant RAM Reduction: ~23% to 60%** depending on attribute count.

📁 **Code:** [03_slots_memory_benchmark.py](file:///c:/Users/ADMIN/Documents/hemant-python/advanced_python/01_advanced_oop/03_slots_memory_benchmark.py)

---

## 4. Top Interview Questions for This Topic

### Q1: What is the difference between an Abstract Base Class (ABC) and a Protocol (`typing.Protocol`)?
* **ABC (Nominal Subtyping):** Enforces inheritance explicitly. A class must inherit from `BaseNotifier` (`class EmailNotifier(BaseNotifier):`).
* **Protocol (Structural Subtyping / Duck Typing):** A class does **not** need to inherit from the Protocol. If it implements the required methods (`send()`), Python considers it valid automatically.

### Q2: Why is Composition preferred over Inheritance in large backend systems?
Inheritance creates tight compile/runtime coupling. If you change a base class, it can break dozens of subclasses across the application. Composition keeps components decoupled, easily mockable in unit tests, and swappable at runtime.

### Q3: What happens if two parent classes define the same method in multiple inheritance?
Python resolves it using **MRO (Method Resolution Order)** via C3 Linearization. The method from the class that appears earlier in the inheritance declaration `class Child(ParentA, ParentB):` takes precedence.

### Q4: When should you NOT use `__slots__`?
1. When you need dynamic runtime attribute assignment (e.g. `obj.new_attribute = "value"` will raise an `AttributeError`).
2. When classes heavily use multiple inheritance without coordinated `__slots__` declarations.
