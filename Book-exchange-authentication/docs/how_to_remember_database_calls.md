# 🧠 How to Remember: `session.get()` vs `session.exec(select())` Forever

> **Quick Reference Guide:** Memory tricks, real-life analogies, and mental rules for technical interviews and daily backend coding.

---

## 🌟 The 3-Second Mental Rule

Whenever you are writing code and wondering:  
*"Should I use `session.get()` or `session.exec(select())`?"*  

Ask yourself just **ONE question**:

> 👉 **"Do I have the ID number in my hand?"**

```
                       Do I have the ID number?
                                  │
                 ┌────────────────┴────────────────┐
                 ▼                                 ▼
             YES! (id = 42)                 NO! (Filter / Condition)
        Use: session.get(Book, 42)     Use: session.exec(select(Book).where(...))
        (One specific person)          (Searching by rules)
```

---

## 🏫 The Real-Life Memory Analogy: School Classroom

Imagine a classroom with 50 students:

### 1. `session.get()` = The Roll Call
* **The Teacher says:** *"Roll Number 12, stand up!"*
* You have the **exact Roll Number (ID)**.
* Only **ONE** student stands up.
* If no student has Roll Number 12, nobody stands up (`None`).

```python
student = session.get(Student, 12)
```

---

### 2. `session.exec(select())` = The Filter Search
* **The Teacher says:** *"Everyone wearing a Blue Shirt, stand up!"*
* You **do NOT have a Roll Number**. You have a **condition** (`shirt == 'Blue'`).
* **MULTIPLE** students can stand up (a list of students).

```python
query = select(Student).where(Student.shirt_color == "Blue")
students = session.exec(query).all()
```

---

## 📊 Quick Translation Table

| What You Want to Do | Question to Ask Yourself | What Code to Write |
| :--- | :--- | :--- |
| **Get Order by URL path (`/orders/5`)** | *"Do I have the ID?"* $\rightarrow$ **YES (5)** | `order = session.get(Order, 5)` |
| **Get Book by URL path (`/books/3`)** | *"Do I have the ID?"* $\rightarrow$ **YES (3)** | `book = session.get(Book, 3)` |
| **Find all unsold books** | *"Do I have the ID?"* $\rightarrow$ **NO (condition `is_sold == False`)** | `session.exec(select(Book).where(Book.is_sold == False)).all()` |
| **Find user by email** | *"Do I have the ID?"* $\rightarrow$ **NO (condition `email == ...`)** | `session.exec(select(User).where(User.email == email)).first()` |
| **Search books by title keyword** | *"Do I have the ID?"* $\rightarrow$ **NO (condition `title.contains(...)`)** | `session.exec(select(Book).where(Book.title.contains("python"))).all()` |
| **Count total orders today** | *"Do I have the ID?"* $\rightarrow$ **NO (aggregation `COUNT`)** | `session.exec(select(func.count(Order.id))).one()` |

---

## 🎯 What to Say in an Interview (The Perfect Answer)

If an interviewer asks:  
> *"What is the difference between `session.get()` and `session.exec(select())`?"*

**Memorize these 3 bullet points:**

1. **`session.get(Model, id)`:**
   * Used for looking up **a single row by its Primary Key (`id`)**.
   * It is ultra-fast because it checks the **in-memory Identity Map cache** first before querying SQLite.
   * Returns the object directly, or `None` if not found.

2. **`session.exec(select(Model).where(...))`:**
   * Used when filtering by **conditions** (like `is_sold == False` or `title LIKE '%python%'`).
   * Used when you expect **a list of multiple rows** (`.all()`).
   * Supports dynamic query chaining (adding `if` conditions in Python before running).

3. **`session.add()` + `commit()`:**
   * Used for **creating new rows** or saving modified attributes (Write operations).
