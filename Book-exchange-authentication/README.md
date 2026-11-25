# 📖 Book Exchange & Authentication API

A peer-to-peer used book marketplace and authentication backend built with **FastAPI**, **SQLModel**, and **SQLite**. Allows college students to register accounts, list second-hand textbooks, search active listings, and update sold statuses—all protected by custom API-Key authentication.

---

## 💡 1. The Core Concept

College textbooks are expensive and often sit unused after a semester ends. 

This platform connects student sellers with buyers on campus:
1. **Students Register:** Create a user profile tied to their college and email.
2. **Students List Books:** Post textbooks with title, author, price, and user ownership.
3. **Buyers Discover:** Search active, unsold books by title or author.
4. **Transactions Completed:** Mark books as sold (`is_sold=True`) when purchased.
5. **Security:** Protected routes require an `x-api-key` request header.

---

## 🛠️ 2. Tech Stack & Architecture

| Layer | Technology | Role |
| :--- | :--- | :--- |
| **Web Framework** | **FastAPI** | High-performance async REST API with auto-generated OpenAPI docs |
| **ORM & Validation** | **SQLModel** | Blends SQLAlchemy (tables & relationships) + Pydantic (data validation) |
| **Database** | **SQLite** (`book-exchange.db`) | Lightweight relational database |
| **Authentication** | **API Key Header** (`x_api_key`) | Header-based gatekeeping for sensitive operations |

---

## 🔗 3. Database Entity Relationship (1-to-Many)

```
 ┌──────────────────────┐               ┌────────────────────────┐
 │      USER TABLE      │               │       BOOK TABLE       │
 ├──────────────────────┤               ├────────────────────────┤
 │ id (PK, int)         │ 1           N │ id (PK, int)           │
 │ name (str, indexed)  │───────────────│ title (str, indexed)   │
 │ email (str, unique)  │               │ author (str, indexed)  │
 │ college (str)        │               │ price (int)            │
 │                      │               │ is_sold (bool)         │
 │                      │               │ user_id (FK -> user.id)│
 └──────────────────────┘               └────────────────────────┘
```

---

## 📡 4. API Endpoints

### 👤 User Endpoints
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `POST` | `/users/` | Registers a new student account | 🔑 Yes (`x-api-key`) |
| `GET` | `/users/` | Lists all registered students | ❌ Public |

### 📚 Book Endpoints
| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :---: |
| `GET` | `/books/` | Lists all active (unsold) books (`?title=`, `?author=`) | ❌ Public |
| `POST` | `/books/` | Creates a new book listing | 🔑 Yes (`x-api-key`) |
| `PATCH` | `/books/{book_id}` | Updates book price or status (`BookUpdate`) | 🔑 Yes (`x-api-key`) |
| `PATCH` | `/books/{book_id}/sold` | Quick-marks a book as sold (`is_sold=True`) | 🔑 Yes (`x-api-key`) |

---

## 📚 5. Deep-Dive Documentation Library

For comprehensive line-by-line breakdowns, under-the-hood mechanics, and senior technical interview questions, see:

* 📖 **[docs/master_project_review.md](file:///c:/Users/ADMIN/Documents/hemant-python/Book-exchange-authentication/docs/master_project_review.md)** — **Master Architecture & Interview Guide**: End-to-end flow, strengths, scaling tips, and resume pitch.
* 📖 **[docs/user_model.md](file:///c:/Users/ADMIN/Documents/hemant-python/Book-exchange-authentication/docs/user_model.md)** — User entity, unique email constraints, `UserCreate` vs `UserRead`, and the One-to-Many relationship.
* 📖 **[docs/book_model.md](file:///c:/Users/ADMIN/Documents/hemant-python/Book-exchange-authentication/docs/book_model.md)** — Book entity, `user_id` Foreign Key vs `owner` Relationship, B-tree indexes, and circular import resolution via `model_rebuild()`.
* 📖 **[docs/user_routes.md](file:///c:/Users/ADMIN/Documents/hemant-python/Book-exchange-authentication/docs/user_routes.md)** — User registration, defensive duplicate email checks, API-key authentication, and Data Mapper patterns.
* 📖 **[docs/book_routes.md](file:///c:/Users/ADMIN/Documents/hemant-python/Book-exchange-authentication/docs/book_routes.md)** — Catalog search with `.contains()`, dynamic query building, partial `setattr` updates, and RPC-style mark-sold transitions.
* 📖 **[docs/how_to_remember_database_calls.md](file:///c:/Users/ADMIN/Documents/hemant-python/Book-exchange-authentication/docs/how_to_remember_database_calls.md)** — The 3-second mental rule, school classroom analogy, and interview cheatsheet for `session.get()` vs `session.exec()`.

---

## 🚀 6. Quickstart

```powershell
# 1. Navigate to directory
cd "c:\Users\ADMIN\Documents\hemant-python\Book-exchange-authentication"

# 2. Start Uvicorn
uvicorn main:app --reload

# 3. Interactive Docs
http://127.0.0.1:8000/docs
```
