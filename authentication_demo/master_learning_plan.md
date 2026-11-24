# Master Curriculum: Advanced Python, SQL Querying & MySQL Engineering

> **Goal:** Transform from a framework consumer into a senior-level Python Backend and Database Engineer capable of designing resilient, high-throughput, and scalable systems.

---

## Table of Contents
1. [Core Curriculum Overview](#1-core-curriculum-overview)
2. [Expert Analysis & Key Additions](#2-expert-analysis--key-additions)
3. [The "Connected Systems" Philosophy](#3-the-connected-systems-philosophy)
4. [Step-by-Step Execution Plan & Checklists](#4-step-by-step-execution-plan--checklists)
   - [Phase 1: Python Advanced Programming](#phase-1-python--advanced-programming)
   - [Phase 2: SQL Advanced Querying](#phase-2-sql--advanced-querying)
   - [Phase 3: MySQL Database Engineering](#phase-3-mysql--database-engineering)
5. [Interview & Practical Milestones](#5-interview--practical-milestones)

---

## 1. Core Curriculum Overview

```
                               MASTER ROADMAP
                               
       ┌──────────────────────────────┼──────────────────────────────┐
       ▼                              ▼                              ▼
┌───────────────┐              ┌───────────────┐              ┌───────────────┐
│ PYTHON EXPERT │              │ SQL ADVANCED  │              │ MYSQL SYSTEMS │
│ • OOP & MRO   │              │ • Window Func │              │ • B-Trees     │
│ • Closures    │              │ • CTEs & Rec  │              │ • EXPLAIN     │
│ • Generators  │              │ • Subqueries  │              │ • Locks/ACID  │
│ • Asyncio/GIL │              │ • Complex Join│              │ • Isolation   │
└───────────────┘              └───────────────┘              └───────────────┘
```

---

## 2. Expert Analysis & Key Additions

### Why This Curriculum is 10/10:
* **High Signal-to-Noise Ratio:** Every topic is a regular fixture in senior coding rounds and systems interviews at FAANG and top product companies.
* **Covers the Entire Backend Lifecycle:**
  * **Python:** Application Runtime, Concurrency, and Memory Management.
  * **SQL:** Data Modeling, Analytical Querying, and Business Logic.
  * **MySQL:** Storage Engine, Execution Plans, and Concurrency Controls.

### 4 Crucial Additions Included in this Plan:
1. **Python Data Model / Dunder Protocol (`__call__`, `__getitem__`, `__slots__`):**
   * *Why:* Powers custom ORMs, dependency injection, and memory optimization (reducing RAM usage by 60%).
2. **Database Migrations (Alembic):**
   * *Why:* In production, `Base.metadata.create_all()` is forbidden. Schema evolution must be version-controlled like Git.
3. **Connection Pooling & Pool Sizing:**
   * *Why:* High concurrency crashes applications not because of CPU, but because MySQL runs out of open connection sockets.
4. **Soft Deletes vs. Hard Deletes & Index Impact:**
   * *Why:* Production systems rarely execute `DELETE FROM`. Handling `deleted_at` timestamps without breaking query indexes is a critical pattern.

---

## 3. The "Connected Systems" Philosophy

To achieve true mastery, do not study these domains as isolated subjects. Combine them:

| Combination | Concept Learned |
| :--- | :--- |
| **Python Generators + SQL Querying** | Stream 1,000,000 database rows with $O(1)$ constant memory usage ($< 30\text{ MB}$ RAM) instead of crashing the server with `fetchall()`. |
| **Python Context Managers + MySQL ACID** | Build atomic transaction managers using `__enter__` and `__exit__` with automatic rollback on unhandled exceptions. |
| **Python Asyncio + MySQL Row Locking** | Use asynchronous coroutines to fire 50 concurrent requests against MySQL to reproduce deadlocks and observe `SELECT ... FOR UPDATE` row locks. |
| **SQL CTEs + MySQL Query Plans** | Compare performance of CTEs vs. Subqueries using MySQL's `EXPLAIN ANALYZE` to inspect temporary tables and filesorts. |

---

## 4. Step-by-Step Execution Plan & Checklists

---

### Phase 1: Python – Advanced Programming

Focus: *Memory Model, Metaprogramming, Asynchronous Execution, and Resilient Architecture.*

- [x] **1. Advanced Object-Oriented Programming (OOP)**
  - [x] Inheritance & Method Resolution Order (MRO / C3 Linearization) via `super()`.
  - [x] Composition over Inheritance ("Has-a" vs. "Is-a" architectures).
  - [x] Abstract Base Classes (`abc.ABC`, `@abstractmethod`) for interface contracts.
  - [x] Polymorphism & Duck Typing (`typing.Protocol` for structural typing).
  - [x] Python Data Model: `__call__` (callable classes), `__repr__`, `__str__`, `__len__`, `__getitem__`.
  - [x] Memory optimization using `__slots__` vs. `__dict__`.

- [x] **2. Decorators & Closures**
  - [x] Lexical scoping, variable capture, and inspecting `func.__closure__`.
  - [x] First-class functions & Higher-Order functions.
  - [x] Writing parameterized decorators (`@retry(max_attempts=3)`).
  - [x] Preserving function metadata with `@functools.wraps`.
  - [x] Class-based decorators vs. Function-based decorators.

- [ ] **3. Iterators, Generators & Context Managers**
  - [ ] The Iterator Protocol (`__iter__` and `__next__`).
  - [ ] Generators, `yield`, and frame suspension in the CPython Virtual Machine.
  - [ ] Two-way generator communication (`generator.send()` and `yield from`).
  - [ ] Context Managers via class protocol (`__enter__` and `__exit__`).
  - [ ] Creating context managers with `@contextlib.contextmanager`.

- [ ] **4. Exception Handling & Custom Exceptions**
  - [ ] Python Exception Hierarchy (`BaseException` vs `Exception`).
  - [ ] Designing clean Domain Exceptions (`UserNotFoundError`, `InsufficientFundsError`).
  - [ ] Exception Chaining (`raise ... from err`) and preserving tracebacks.
  - [ ] Best practices for `try / except / else / finally`.

- [ ] **5. Concurrency: Multithreading, Multiprocessing & Async/Await**
  - [ ] The Global Interpreter Lock (GIL): Why it exists and how it affects execution.
  - [ ] CPU-bound vs. I/O-bound workloads.
  - [ ] `threading` & ThreadPoolExecutor for I/O operations.
  - [ ] `multiprocessing` & ProcessPoolExecutor for CPU-heavy tasks.
  - [ ] `asyncio` Event Loop, Coroutines, Tasks, and `asyncio.gather`.
  - [ ] Async Context Managers (`async with`) and Async Iterators (`async for`).

- [ ] **6. File Handling & Streaming**
  - [ ] Parsing and generating CSV and JSON with robust error handling.
  - [ ] Working with Excel (`openpyxl` / `pandas`).
  - [ ] Processing massive files (10GB+) line-by-line using generator chunking.

- [ ] **7. Production Logging & Debugging**
  - [ ] Built-in `logging` module: Loggers, Handlers, Formatters, and Filters.
  - [ ] Rotating file handlers and structured JSON logging.
  - [ ] Debugging with `pdb` / `breakpoint()` and interpreting CPython tracebacks.

---

### Phase 2: SQL – Advanced Querying

Focus: *Analytical Power, Set Theory, and Complex Data Retrieval.*

- [ ] **1. Joins & Relational Sets**
  - [ ] `INNER JOIN`, `LEFT OUTER JOIN`, `RIGHT OUTER JOIN`, `FULL OUTER JOIN`.
  - [ ] `CROSS JOIN` (Cartesian Product) and `SELF JOIN` (Hierarchical tree structures).
  - [ ] Anti-joins (`LEFT JOIN ... WHERE right.id IS NULL`) vs `NOT EXISTS`.

- [ ] **2. Subqueries & Correlated Subqueries**
  - [ ] Scalar subqueries, Column subqueries, and Row subqueries.
  - [ ] Correlated Subqueries: Execution mechanics (row-by-row re-evaluation).
  - [ ] Subqueries in `SELECT`, `FROM`, and `WHERE` clauses.
  - [ ] `EXISTS` vs `IN` performance differences.

- [ ] **3. Common Table Expressions (CTEs)**
  - [ ] Non-Recursive CTEs for readable, modular SQL queries.
  - [ ] Recursive CTEs (traversing organizational charts, categories, and graphs).
  - [ ] Comparing CTE performance against temporary tables.

- [ ] **4. Window Functions (Analytical SQL)**
  - [ ] The `OVER()` clause, `PARTITION BY`, and `ORDER BY`.
  - [ ] Ranking functions: `ROW_NUMBER()`, `RANK()`, `DENSE_RANK()`.
  - [ ] Value functions: `LEAD()`, `LAG()` (finding month-over-month differences).
  - [ ] Cumulative functions: `SUM() OVER (...)`, Moving Averages.

- [ ] **5. Conditional Logic: CASE Statements**
  - [ ] Simple `CASE` vs. Searched `CASE`.
  - [ ] Pivoting data rows into columns using `CASE` inside aggregations.
  - [ ] Conditional sorting and filtering.

- [ ] **6. Stored Procedures, Functions & Triggers**
  - [ ] Stored Procedures with `IN`, `OUT`, and `INOUT` parameters.
  - [ ] User-Defined Functions (UDFs) vs Built-in functions.
  - [ ] Triggers (`BEFORE INSERT`, `AFTER UPDATE`) for automated auditing.
  - [ ] Trade-offs: Database logic vs Application logic.

- [ ] **7. Database Views**
  - [ ] Standard Views for security abstraction and query reuse.
  - [ ] Materialized Views (concepts, refresh patterns, and performance).

---

### Phase 3: MySQL – Database Engineering

Focus: *Storage Engines, Execution Plans, Concurrency Controls, and Reliability.*

- [ ] **1. Indexing & Storage Engine Architecture**
  - [ ] InnoDB Architecture: Clustered Index (Primary Key) vs Secondary Indexes.
  - [ ] B-Tree Index internal structure (leaf nodes, branch nodes, page splits).
  - [ ] Single-column indexes vs Composite (Multi-column) indexes.
  - [ ] The Leftmost Prefix Rule in composite indexes.
  - [ ] Covering Indexes (Index-Only Scans) to eliminate table lookups.

- [ ] **2. Query Optimization & `EXPLAIN` Plans**
  - [ ] Interpreting `EXPLAIN` and `EXPLAIN ANALYZE` output.
  - [ ] Key metrics: `type` (`ALL`, `index`, `range`, `ref`, `const`), `rows`, `filtered`.
  - [ ] Spotting performance red flags: `Using filesort`, `Using temporary`.
  - [ ] MySQL Slow Query Log setup and query profiling.

- [ ] **3. Transactions & ACID Guarantees**
  - [ ] **A**tomicity: Undo Log and rollback mechanics.
  - [ ] **C**onsistency: Foreign keys and database integrity rules.
  - [ ] **I**solation: Read phenomena (Dirty Read, Non-repeatable Read, Phantom Read).
  - [ ] **D**urability: Redo Log, Write-Ahead Logging (WAL), and `fsync`.

- [ ] **4. Transaction Isolation Levels & Locking**
  - [ ] Isolation levels: `READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, `SERIALIZABLE`.
  - [ ] InnoDB default (`REPEATABLE READ`) and MVCC (Multi-Version Concurrency Control).
  - [ ] Row-Level Locks: Shared (`LOCK IN SHARE MODE`) vs Exclusive (`FOR UPDATE`).
  - [ ] Gap Locks & Next-Key Locks (preventing phantom rows).
  - [ ] Detecting, analyzing, and preventing Deadlocks.

- [ ] **5. Schema Normalization & Key Constraints**
  - [ ] 1NF (Atomic values), 2NF (No partial dependencies), 3NF (No transitive dependencies).
  - [ ] When and how to Denormalize for read-heavy performance.
  - [ ] Primary Keys (Auto-Increment vs UUIDv4 / UUIDv7 vs ULID).
  - [ ] Foreign Keys with `ON DELETE CASCADE`, `ON DELETE SET NULL`, `RESTRICT`.

- [ ] **6. Production Operations: Backup & Recovery**
  - [ ] Logical backups (`mysqldump`, `mydumper`).
  - [ ] Physical backups (Percona XtraBackup).
  - [ ] Point-in-time recovery using MySQL Binary Logs (`binlog`).

---

## 5. Interview & Practical Milestones

By completing this roadmap, you will be prepared to answer:
1. *How does CPython's garbage collector handle cyclic references, and why does `__del__` complicate it?*
2. *What is the exact execution difference between `DENSE_RANK()` and `RANK()`?*
3. *Why does `SELECT COUNT(*)` on InnoDB require a full scan, while MyISAM returned it in $O(1)$?*
4. *How does MySQL handle deadlocks between two concurrent transactions updating rows in opposite order?*
5. *Why does adding an index sometimes make `INSERT` and `UPDATE` queries slower?*
