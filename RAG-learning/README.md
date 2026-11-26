# 🤖 RAG & LangChain Learning Lab

A complete, production-grade, and **100% free** implementation of a **Retrieval-Augmented Generation (RAG)** pipeline powered by **LangChain**, **FastEmbed**, **Qdrant Vector Database**, **FastAPI**, and **Google Gemini**.

> 🏛️ **[docs/00_master_architecture_and_execution_flow.md](docs/00_master_architecture_and_execution_flow.md)** &mdash; Full System Architecture Diagrams, End-to-End Execution Sequence, and Component Interaction Map.

---

## 💡 1. System Architecture

```text
================================ INGESTION PIPELINE (app/index.py) ================================
  [PDF Document] ──> [PyPDFLoader] ──> [RecursiveCharacterTextSplitter] ──> [FastEmbed (384-dim)] ──> [Qdrant DB]
   (sample.pdf)         (Pages)             (Chunks of 1000 chars)          (bge-small-en-v1.5)        (:6333)

================================= QUERY & RAG PIPELINE (FastAPI) =================================
  [User Question]
        │
        ▼
  [FastEmbed] ──> Vector Search ──> [Qdrant DB] ──> [Top-K Relevant Chunks (Page Numbers & Scores)]
                                                              │
                                                              ▼
                                                   [Context + System Prompt]
                                                              │
                                                              ▼
                                                [Google Gemini (gemini-3.5-flash-lite)]
                                                              │
                                                              ▼
                                                [Final Answer with Page Citations]
```

---

## 🛠️ 2. Tech Stack & Cost Overview

| Component | Technology | Role | Cost / Limits |
| :--- | :--- | :--- | :--- |
| **Vector Database** | **Qdrant** | Stores & queries 384-dim dense vectors with HNSW indexing | **Free** (Local Docker container on port `6333`) |
| **Containerization**| **Docker Desktop** | Runs Qdrant with persistent disk volume storage | **Free** |
| **Embeddings** | **FastEmbed** (`BAAI/bge-small-en-v1.5`) | Generates semantic embeddings locally on CPU | **100% Free** (No API keys, no network calls, zero rate limits) |
| **LLM (Generation)**| **Google Gemini** (`gemini-3.5-flash-lite`) | Synthesizes grounded answers citing exact page numbers | **Free Tier** (15 RPM / 1M TPM via Google AI Studio) |
| **API Backend** | **FastAPI + Uvicorn** | High-performance async REST API with auto-generated Swagger UI | **Free** (`http://127.0.0.1:8000/docs`) |
| **Orchestration** | **LangChain** | Connects loaders, chunkers, vector store, and LLM chains | **Free** |

---

## 📂 3. Project Structure

```text
RAG-learning/
├── .env                       # Environment variables (GEMINI_API_KEY)
├── docker-compose.yml         # Qdrant vector database container definition
├── main.py                    # FastAPI root application entry point
├── README.md                  # Master project guide & documentation
├── requirements.txt           # Python project dependencies
├── app/
│   ├── .env                   # Local app environment copy
│   ├── index.py               # Ingestion script (PDF -> Chunks -> Embeddings -> Qdrant)
│   ├── query.py               # CLI tool to test vector similarity search directly
│   ├── data/
│   │   └── sample.pdf         # Source document (e.g., 241-page textbook)
│   └── routes/
│       └── query_routes.py    # POST /query/ API route with Gemini RAG generation
├── docs/
│   ├── 01_rag_fundamentals.md # Deep dive: Open-Book Exam analogy, RAG vs Fine-tuning, math & diagrams
│   └── 02_langchain_guide.md  # Deep dive: 5 pillars of LangChain, LCEL, code examples
└── qdrant_storage/            # Persistent storage volume for Qdrant vectors
```

---

## 🚀 4. Step-by-Step Setup & Running Guide

### Step 1: Start Qdrant Vector Database

```powershell
# Navigate to the project root
cd C:\Users\ADMIN\Documents\hemant-python\RAG-learning

# Launch Qdrant in Docker
docker compose up -d

# Verify Qdrant is running
docker ps
```
* Interactive Web Dashboard: **`http://localhost:6333/dashboard`**

---

### Step 2: Configure Your Free Gemini API Key

1. Get your free key from **[Google AI Studio](https://aistudio.google.com/apikey)** (no credit card required).
2. Add it to your `.env` file:
   ```env
   GEMINI_API_KEY=AIzaSyYourGeneratedKeyHere
   ```

---

### Step 3: Index Documents into Qdrant

Whenever you add or update documents in `app/data/sample.pdf`, run the indexer:

```powershell
python -m app.index
```

**What happens:**
* Loads the PDF via `PyPDFLoader`.
* Splits text using `RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=400)`.
* Computes 384-dimensional dense vectors using FastEmbed on your CPU.
* Ingests all points into Qdrant collection `sample_collection`.

---

### Step 4: Run the FastAPI Web Server

```powershell
fastapi dev
```
*(Or if running from parent directory: `fastapi dev RAG-learning/main.py`)*

* **API Base:** `http://127.0.0.1:8000`
* **Interactive Swagger UI:** **`http://127.0.0.1:8000/docs`**

---

## 📡 5. API Reference

### `POST /query/`
Performs semantic similarity retrieval from Qdrant, augments context with page metadata, and generates an answer via Google Gemini.

#### Request Body
```json
{
  "question": "what is http?"
}
```

#### Response Body (`200 OK`)
```json
{
  "question": "what is http?",
  "answer": "Based on the provided context, HTTP stands for Hypertext Transfer Protocol (Page 205). It is frequently employed for client/server web-based interactions and offers a stateless communication mechanism appropriate for a variety of uses (Page 144).",
  "sources": [
    {
      "page": 205,
      "similarity_score": 0.6131,
      "content": "Glossary\n● HTTP: Hypertext Transfer Protocol\n● REST: Representational State Transfer\n● API: Application programming interface..."
    },
    {
      "page": 144,
      "similarity_score": 0.6611,
      "content": "a. HTTP/HTTPS: Frequently employed for client/server web-based interactions. offers a stateless communication mechanism..."
    }
  ]
}
```

---

## 📚 6. Deep-Dive Documentation Library

### 🗂️ File-by-File Master Study Guides:
* 🐳 **[`docker-compose.yml` Guide](docs/03_step1_docker_and_qdrant.md)**  
  * *Docker containers, ports 6333 vs 6334, persistent storage volumes, cargo ship analogy, and interview Q&A.*
* 📄 **[`app/index.py` Complete Guide](docs/04_file_guide_app_index_py.md)**  
  * *The complete ingestion pipeline: PyPDFLoader, RecursiveCharacterTextSplitter (1000/400), FastEmbed 384-dim embeddings, Qdrant collection recreation, GPS analogy, and interview Q&A.*
* 🔍 **[`app/query.py` Complete Guide](docs/05_file_guide_app_query_py.md)**  
  * *Developer diagnostic tool, CLI retrieval testing, Cosine Similarity math, top-k tuning, library index card analogy, and interview Q&A.*
* ⚡ **[`app/routes/query_routes.py` Complete Guide](docs/06_file_guide_query_routes_py.md)**  
  * *The production RAG engine: FastAPI endpoint, Pydantic v2 schemas, anti-hallucination prompt engineering, Google Gemini generation, research assistant analogy, and interview Q&A.*
* 🚪 **[`main.py` Complete Guide](docs/07_file_guide_main_py.md)**  
  * *Application gateway: FastAPI factory, APIRouter modular mounting, ASGI async concurrency vs WSGI, OpenAPI auto-docs, hotel lobby analogy, and interview Q&A.*
* 🔐 **[`.env` Complete Guide](docs/08_file_guide_env.md)**  
  * *Secrets management: Twelve-Factor App config, why never hardcode keys, .env.example templates, .gitignore safety net, emergency leak recovery, hidden safe analogy, and interview Q&A.*

### 📖 Concept Reference Library:
* 📖 **[docs/01_rag_fundamentals.md](docs/01_rag_fundamentals.md)**  
  * *Open-Book Exam analogy, RAG vs Fine-Tuning matrix, Dark Mode Ingestion & Querying pipelines, GPS embedding analogy, core terminology, and Top 10 Senior Interview Q&A.*
* 📖 **[docs/02_langchain_guide.md](docs/02_langchain_guide.md)**  
  * *LangChain architecture, why use it over raw Python, 5 core pillars, Qdrant integration code, LCEL pipe syntax (`|`), and Top Interview Q&A.*

---

## ✅ 7. Roadmap & Progress

- [x] **Vector Database Setup:** Dockerized Qdrant container running with persistent volume.
- [x] **Local Embedding Ingestion:** 100% Free local embedding pipeline using FastEmbed (`BAAI/bge-small-en-v1.5`).
- [x] **Large Document Indexing:** Split and embedded 241-page textbook into 1,173 indexed vector points.
- [x] **FastAPI REST API:** Full async API with Pydantic request/response schemas.
- [x] **LLM Answer Generation:** Integrated free Google Gemini (`gemini-3.5-flash-lite`) with source citations.
- [x] **High-Recall Retrieval:** Configured `k=10` retrieval to capture both in-depth chapters and glossary definitions.
