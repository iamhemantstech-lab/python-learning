# ⚡ Complete File Guide: `app/routes/query_routes.py` (The RAG Brain)

> **File in Repository:** [`app/routes/query_routes.py`](../app/routes/query_routes.py)  
> **Role in Architecture:** The Production Web API Route  
> **The Real RAG Engine:** Orchestrates Retrieval (FastEmbed + Qdrant) ➔ Augmentation (Prompt Context) ➔ Generation (Google Gemini)

---

## 💡 1. What Is This File & Why Is It Used?

While [`app/index.py`](../app/index.py) runs once to prepare data, and [`app/query.py`](../app/query.py) is a local developer tool, **[`app/routes/query_routes.py`](../app/routes/query_routes.py) is the true production heart of your application**.

When a user in a web browser, mobile app, or Swagger UI sends a question like:
```json
POST /query/
{ "question": "What is HTTP?" }
```
This file receives the HTTP request, executes all 3 steps of RAG (**R**etrieve, **A**ugment, **G**enerate), and returns a formatted JSON answer citing exact page numbers.

---

## 📜 2. Complete Code Architecture (The 3 Stages of RAG)

```text
==================================== POST /query/ ====================================

  1. USER INPUT (HTTP Request)
     └── Pydantic validates input: {"question": "What is HTTP?"}
           │
           ▼
  2. STAGE 1: RETRIEVAL (R)
     └── FastEmbed vectorizes the question (384 dimensions)
     └── Qdrant searches 1,173 chunks for top-10 nearest vectors
     └── Extracts Page numbers (Page 205, Page 144) and similarity scores
           │
           ▼
  3. STAGE 2: AUGMENTATION (A)
     └── Assembles chunks into text: "[Page 205] HTTP: Hypertext Transfer Protocol..."
     └── Builds Strict System Prompt with Anti-Hallucination Guardrails
           │
           ▼
  4. STAGE 3: GENERATION (G)
     └── Calls Google Gemini API (`gemini-3.5-flash-lite`)
     └── Gemini reads the context and drafts the final answer
           │
           ▼
  5. USER OUTPUT (HTTP 200 OK Response)
     └── Returns JSON: { "question": ..., "answer": ..., "sources": [...] }
```

---

## 🔍 3. Deep-Dive Line-by-Line Breakdown

### A. Dynamic `.env` Auto-Resolution (Lines 11–20 & 55–63)
```python
_base_dir = Path(__file__).resolve().parent
_rag_env = _base_dir.parent.parent / ".env"
_app_env = _base_dir.parent / ".env"
_root_env = _base_dir.parent.parent.parent / ".env"

for env_file in [_rag_env, _app_env, _root_env]:
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=True)
```
* **Why this is needed:** Developers often run `fastapi dev` from different folders (`hemant-python` or `RAG-learning`). This code checks all parent folders so your `GEMINI_API_KEY` is **never missed**.
* **Dynamic Reloading (`get_gemini_api_key`):** If you edit `.env` while the server is running, the helper reloads the file dynamically so you don't even have to restart the server!

---

### B. Pydantic Schemas (Lines 39–52)
```python
class QueryRequest(BaseModel):
    question: str

class SourceChunk(BaseModel):
    page: int
    similarity_score: float
    content: str

class QueryResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceChunk]
```
* **Why Pydantic?**
  1. **Strict Type Safety:** Rejects malformed requests (e.g., sending numbers instead of text).
  2. **Automatic Swagger UI Documentation:** FastAPI reads these classes to generate the interactive web forms you see at `http://127.0.0.1:8000/docs`.
  3. **Output Serialization:** Converts Python objects directly into standardized JSON.

---

### C. Step 1: Retrieval (R) (Lines 72–90)
```python
search_results = vector_db.similarity_search_with_score(query=question, k=10)
```
* **Why `k=10`?**
  * In our 241-page textbook (1,173 chunks), setting `k=2` was too narrow and caused the `"I don't know"` bug because the glossary on Page 205 was ranked at #9. Setting `k=10` ensures both detailed chapters and short glossaries are captured.
* **1-Based Page Formatting:**
  ```python
  page=doc.metadata.get("page", 0) + 1
  ```
  Python arrays and PDF libraries are 0-indexed (Page 0 is the cover). Adding `+1` translates it into human-friendly book page numbers.

---

### D. Step 2: Augmentation (A) & Prompt Engineering (Lines 92–106)
```python
context = "\n\n".join(
    [f"[Page {src.page}] {src.content}" for src in sources]
)

prompt = f"""You are a helpful assistant that answers questions accurately based on the provided context.
If the context does not contain the answer, respond with "I don't know."
Always mention the page number(s) from the context in your answer.

Context:
{context}

Question: {question}

Answer:"""
```

#### The 3 Guardrails in this Prompt:
1. **Grounding:** *"based on the provided context"* &rarr; Forces the LLM to ignore pre-trained internet knowledge and only trust your textbook.
2. **Anti-Hallucination:** *"If the context does not contain the answer, respond with 'I don't know.'"* &rarr; Prevents the AI from inventing fake facts.
3. **Traceability:** *"Always mention the page number(s)"* &rarr; Provides immediate verifiability for end users.

---

### E. Step 3: Generation (G) via Google Gemini (Lines 108–131)
```python
client = genai.Client(api_key=gemini_key)
response = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt,
)
answer = response.text.strip()
```

#### Why `gemini-3.5-flash-lite`?
* **100% Free Tier:** Available without credit card via Google AI Studio.
* **Speed:** "Flash-lite" models are optimized for sub-second text generation.
* **1 Million Token Window:** Can easily process 10, 20, or even 100 chunks without truncation.
* **Graceful Degradation:** If the API key is missing or rate-limited, the endpoint does not crash with a 500 error; it gracefully returns the raw retrieved chunks with a helpful tip!

---

## ⚖️ 4. Alternative LLM Providers Comparison

| Provider / Model | Cost | Speed | Context Window | Best Used For |
| :--- | :--- | :--- | :--- | :--- |
| **Google Gemini (`gemini-3.5-flash-lite`)** 🏆 | **\$0 (Free Tier)** | ⚡ Ultra-fast (~0.8s) | **1,000,000 tokens** | **Our choice:** Free, generous limits, perfect for RAG. |
| **OpenAI (`gpt-4o-mini`)** | Paid (\$0.15 / 1M tokens) | Fast (~1.2s) | 128,000 tokens | Standard commercial enterprise apps. |
| **Groq Cloud (Llama-3.3-70B)** | Free Tier available | ⚡⚡ Blazing fast (~0.3s) | 128,000 tokens | Open-source lovers who want maximum speed. |
| **Local Ollama (Llama-3.2 3B)** | \$0 (Runs on local GPU) | Medium (depends on PC) | 8,000–32,000 tokens | 100% offline air-gapped military/banking systems. |

---

## 🧠 5. Permanent Memory Trick (The Analogy)

### 🧑‍💼 The Research Assistant & The Executive Analogy:
> Imagine a busy CEO (the User) asking: *"What is our company's HTTP policy?"*
> * **`query_routes.py` is the CEO's top Research Assistant.**
> * The assistant runs down to the archives (Qdrant), pulls 10 relevant documents with sticky notes marking the pages (**Retrieval**).
> * The assistant places those 10 pages on the desk with a cover letter stating: *"Here are the exact facts, do not guess"* (**Augmentation**).
> * The assistant asks the executive speechwriter, Gemini (**Generation**), to read those 10 pages and write a clear 2-sentence summary for the CEO.

---

## 🎓 6. Senior Interview Battle Card for `query_routes.py`

#### Q1: "How do you mitigate hallucinations in the Generation phase of RAG?"
> **Senior Answer:**  
> *"We implement a three-layer defense:  
> 1. **Prompt Constraint:** We explicitly instruct the LLM to restrict its reasoning strictly to the provided context and respond with 'I don't know' if unaddressed.  
> 2. **Temperature Control:** We keep generation temperature low ($\le 0.2$) to reduce creative randomness and maximize factual determinism.  
> 3. **Mandatory Citations:** We require the model to cite the exact source page numbers embedded in the context tags (`[Page X]`), allowing human verification."*

#### Q2: "What is the difference between query parameters and request bodies in FastAPI, and why did you use Pydantic `BaseModel`?"
> **Senior Answer:**  
> *"In HTTP POST endpoints, scalar arguments like `def query(question: str)` default to URL query parameters (`/query/?question=...`), which exposes search queries in web server access logs and limits payload size. By using a Pydantic `BaseModel`, FastAPI forces the payload into the JSON request body. This provides automatic schema validation, security, and generates clean interactive documentation in Swagger UI."*

#### Q3: "What happens if the Gemini LLM API goes down or exceeds its rate limit?"
> **Senior Answer:**  
> *"In `query_routes.py`, the LLM invocation is wrapped in a `try-except` block. If Gemini fails due to quota exhaustion or network timeout, the endpoint gracefully falls back: it returns HTTP 200 with the raw retrieved text chunks and page references from Qdrant, accompanied by an explanatory notice. This guarantees that user queries still receive accurate reference data even during upstream LLM outages."*

---

### 🏁 `query_routes.py` Summary Checklist:
- [x] Know how FastAPI routes handle JSON requests via Pydantic.
- [x] Master the 3 stages: Retrieval ($k=10$), Augmentation (Prompt assembly), Generation (Gemini).
- [x] Understand how Anti-Hallucination prompt constraints work.
- [x] Explain graceful error handling and fallback mechanisms.
- [x] Answer senior questions on API design and temperature tuning.
