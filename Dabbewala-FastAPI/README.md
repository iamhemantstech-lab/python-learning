# 🍱 Dabbawala Delivery API

A fast, lightweight order management and lunchbox delivery tracking backend inspired by Mumbai's legendary **Dabbawala** delivery network. Built with **FastAPI**, **SQLModel**, and **SQLite**.

---

## 💡 1. The Core Concept

In Mumbai, thousands of *Dabbawalas* collect hot, home-cooked lunchboxes (dabbas) from customers' homes or central cloud kitchens and deliver them directly to office desks with near-zero error rates.

This API digitizes that delivery lifecycle:
* **Customers / Kitchens** place orders.
* **Operations Teams** track orders through strict delivery states.
* **Management Dashboards** view live daily analytics.

---

## 🔄 2. End-to-End Delivery Flow

```
 [1. CUSTOMER PLACES ORDER]
 POST /orders/
 Payload: {"customer_name": "Pankaj", "delivery_address": "BKC", "items": "Thali"}
              │
              ▼
    State: PREPARING  ──► (Kitchen cooks & packs the dabba)
              │
              ▼
    State: PICKED_UP  ──► (Dabbawala collects the dabba)
              │
              ▼
    State: IN_TRANSIT ──► (Dabbawala on train/bicycle to office)
              │
              ▼
    State: DELIVERED  ──► (Dabba delivered to office desk)
              │
              ▼
 [2. OPERATIONS & METRICS]
 GET /orders/?status=preparing   ──► Find pending dabbas
 GET /stats/daily                ──► Daily volume & status counts
```

---

## ✨ 3. Core Features

* **⚡ Unified Model Architecture:** Uses **SQLModel** (combining SQLAlchemy + Pydantic) to eliminate duplicate code for tables and validation.
* **📦 Order Management:** Create orders, list orders, and filter by status (`preparing`, `picked_up`, `in_transit`, `delivered`).
* **📅 Date Range Filtering:** Automatically captures 24-hour single-day ranges using `datetime.combine()`.
* **🛡️ Defensive Pagination:** Built-in limits (`ge=1, le=100`) preventing server memory exhaustion.
* **📊 Optimized Analytics:** Database-level aggregations (`func.count()`) in $O(1)$ memory.
* **🩺 Production Health Check:** Dedicated `/health` endpoint for load balancers.
* **📖 Auto-Generated Documentation:** Interactive Swagger UI at `/docs`.

---

## 🛠️ 4. Tech Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Web Framework** | **FastAPI** | High-performance ASGI REST API |
| **ORM & Validation** | **SQLModel** | Unified SQLAlchemy tables + Pydantic schemas |
| **Database** | **SQLite** (`dabbawala.db`) | Zero-configuration relational database |
| **Server** | **Uvicorn** | Lightning-fast ASGI web server |

---

## 📡 5. API Endpoints Summary

| Method | Endpoint | Description | Status |
| :--- | :--- | :--- | :---: |
| `GET` | `/health` | Server health check (`{"status": "ok"}`) | ✅ Live |
| `POST` | `/orders/` | Creates a new order (defaults to `preparing`) | ✅ Live |
| `GET` | `/orders/` | Lists orders with filters (`?status=`, `?created_date=`, `?skip=`, `?limit=`) | ✅ Live |
| `GET` | `/stats/daily` | Returns daily summary aggregated by status (`?summary_date=`) | ✅ Live |

---

## 🔮 6. Upcoming Feature Development (Roadmap)

The following features have their schemas prepared in [models.py](file:///c:/Users/ADMIN/Documents/hemant-python/Dabbewala-FastAPI/models.py) and are queued for implementation:

- [ ] **Single Order Lookup (`GET /orders/{order_id}`)**:
  - Retrieve details for a specific order by ID with `404 Not Found` handling.
- [ ] **Partial Order Updates (`PATCH /orders/{order_id}`)**:
  - Uses `OrderUpdate` (`status`, `delivery_address`) with `exclude_unset=True` to update fields without overwriting unchanged data.
- [ ] **Delivery Timeline & Audit Logging (`StatusLog`)**:
  - Track delivery state changes (`old_status` $\rightarrow$ `new_status`, `changed_at`) for live package tracking history.
- [ ] **Order Cancellation (`DELETE /orders/{order_id}`)**:
  - Soft-delete or remove cancelled orders from active delivery runs.

---

## 🚀 7. Quickstart Guide

### 1. Start the Server:
```powershell
uvicorn main:app --reload
```

### 2. Open Interactive Documentation:
Visit in your browser:
* **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📚 8. Deep-Dive Documentation Library

For line-by-line breakdowns, under-the-hood concepts, and interview questions, see:

* 📖 **[01_models.md](file:///c:/Users/ADMIN/Documents/hemant-python/Dabbewala-FastAPI/docs/01_models.md)** — Enums, SQLModel tables, DTOs, and timestamps.
* 📖 **[02_database.md](file:///c:/Users/ADMIN/Documents/hemant-python/Dabbewala-FastAPI/docs/02_database.md)** — SQLite connection engine and session lifecycle (`yield`).
* 📖 **[03_routes_orders.md](file:///c:/Users/ADMIN/Documents/hemant-python/Dabbewala-FastAPI/docs/03_routes_orders.md)** — Order creation, pagination, and date range filtering.
* 📖 **[04_routes_stats.md](file:///c:/Users/ADMIN/Documents/hemant-python/Dabbewala-FastAPI/docs/04_routes_stats.md)** — SQL `func.count()`, grouping, and dynamic date defaults.
* 📖 **[05_main.md](file:///c:/Users/ADMIN/Documents/hemant-python/Dabbewala-FastAPI/docs/05_main.md)** — Lifespan context managers, router mounting, and `/health`.
