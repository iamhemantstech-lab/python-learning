# 🔍 Complete File Guide: `app/query.py` (Local Diagnostic Tool)

> [!IMPORTANT]
> **HOW TO EASILY DIFFERENTIATE THIS FILE:**
> * **`app/query.py` = LOCAL DIAGNOSTIC & TESTING TOOL ONLY.**  
>   It is an optional CLI script used by developers to test Qdrant vector retrieval directly in your PowerShell terminal ($0 cost, no LLM, no web server needed).
> * **`app/routes/query_routes.py` = THE ACTUAL PRODUCTION API ROUTE.**  
>   This is the real web endpoint that FastAPI uses to retrieve context and call Google Gemini to generate answers.
> * **Key Note:** Your web application (`fastapi dev`) does **not** depend on `query.py`. It runs 100% properly without it!

> **File in Repository:** [`app/query.py`](../app/query.py)  
> **Role in Architecture:** Developer Retrieval Diagnostic Utility  
> **Purpose:** Inspect vector search results, cosine similarity scores, and page metadata directly from the terminal.

---

## 💡 1. What Is `app/query.py` & Why Is It Used?

In production AI development, **never connect an LLM until you have verified your retrieval step in isolation**.

If your RAG application gives a bad answer, you must know:
* *Is the LLM hallucinating?* **OR**
* *Did the Vector Database return the wrong chunks?*

[`app/query.py`](../app/query.py) solves this. It bypasses the LLM and talks directly to Qdrant. It embeds your question, calculates mathematical cosine distance against all 1,173 indexed chunks, and prints the top matching chunks along with their **exact similarity scores** and **page numbers**.

---

## 📜 2. Complete Code Walkthrough (Line-by-Line)

Here is your exact file: [`app/query.py`](../app/query.py):

```python
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import QdrantVectorStore

# Load environment variables
load_dotenv()

def main():
    # 1. Initialize the EXACT SAME local embedding model used for indexing
    print("Loading local embedding model (BAAI/bge-small-en-v1.5)...")
    embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

    # 2. Connect to the existing Qdrant collection
    print("Connecting to Qdrant at http://localhost:6333...")
    vector_store = QdrantVectorStore.from_existing_collection(
        embedding=embedding_model,
        collection_name="sample_collection",
        url="http://localhost:6333",
    )

    # 3. Read query from command line arguments or use default
    query_text = "What is HTTP?"
    if len(sys.argv) > 1:
        query_text = " ".join(sys.argv[1:])

    print(f"\n[User Query]: \"{query_text}\"")
    print("=" * 60)

    # 4. Perform Vector Similarity Search with Scores (Cosine Similarity)
    results_with_score = vector_store.similarity_search_with_score(query=query_text, k=5)

    print(f"Retrieved {len(results_with_score)} most relevant chunk(s) from Qdrant:\n")
    for idx, (doc, score) in enumerate(results_with_score, start=1):
        page_num = doc.metadata.get("page", 0) + 1
        print(f"--- [Result #{idx}] | Similarity Score: {score:.4f} | Page: {page_num} ---")
        print(doc.page_content.strip()[:400] + ("..." if len(doc.page_content) > 400 else ""))
        print("-" * 60)

if __name__ == "__main__":
    main()
```

---

## 🔍 3. Deep-Dive into the Core Concepts

### A. `from_existing_collection` vs. `from_documents`
* In `app/index.py`, we used `QdrantVectorStore.from_documents(...)` because we were **creating and writing** data.
* In `app/query.py`, we use `QdrantVectorStore.from_existing_collection(...)` because the database is **already populated**. This performs a lightweight read-only connection without re-uploading or wiping anything.

---

### B. Golden Rule of Vector Search: Symmetric Embeddings
Notice line 12:
```python
embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")
```
> [!IMPORTANT]
> **The Cardinal Rule of Vector Search:**  
> The model used to embed the user's question **MUST BE IDENTICAL** to the model used to embed the document chunks during indexing.

* **What happens if you violate this?**
  * If you index chunks with FastEmbed (384 dimensions) and query with OpenAI (3072 dimensions), Qdrant rejects the query immediately with a dimension mismatch error.
  * Even if two models share the same dimension count, their internal neural coordinate systems are completely different. A vector for "cat" in Model A might mean "refrigerator" in Model B!

---

### C. `similarity_search_with_score` & Cosine Math

In line 32:
```python
results_with_score = vector_store.similarity_search_with_score(query=query_text, k=5)
```

#### What does `k=5` mean?
$k$ represents the **Top-K Nearest Neighbors**. It instructs Qdrant: *"Find the 5 vectors in your 384-dimensional database that have the smallest angle to the user's question vector."*

#### What does the Similarity Score mean?
Qdrant calculates **Cosine Similarity**, which measures the cosine of the angle between two multi-dimensional vectors:

$$\text{Cosine Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}$$

* **Score = 1.0 (Angle = $0^\circ$):** Exact mathematical match.
* **Score $\ge$ 0.65:** Strong semantic relevance (e.g., our search for `"What is HTTP?"` matched Page 144 with **`0.6611`**).
* **Score $\le$ 0.40:** Irrelevant noise (words have very little semantic relationship).

---

## ⚖️ 4. Alternative Search Algorithms in Vector Databases

When interviewing, demonstrating knowledge of search variations proves seniority:

| Search Method | How It Works | When to Use |
| :--- | :--- | :--- |
| **Standard Similarity Search (Our Choice)** 🏆 | Returns top-$k$ vectors with highest cosine similarity | General fact lookup and straightforward QA. |
| **Similarity Search with Score Threshold** | Only returns chunks if `score >= 0.60` | When you want to prevent the LLM from receiving low-quality noise. |
| **Maximum Marginal Relevance (MMR)** | Balances relevance with **diversity** (penalizes redundant chunks) | Summaries or research queries where you don't want 3 chunks repeating the same paragraph. |
| **Hybrid Search (Dense + Sparse BM25)** | Combines semantic vector search with exact keyword matching | Search across product codes, SKUs, or medical terms where exact spelling matters. |

---

## 🛠️ 5. How to Run & Use `app/query.py`

You can run this CLI tool anytime directly from PowerShell without starting Docker UI or the web server:

```powershell
# Navigate to the project root
cd C:\Users\ADMIN\Documents\hemant-python\RAG-learning

# Query with default question ("What is HTTP?")
python -m app.query

# Query with any custom question from your textbook
python -m app.query "What are the advantages of microservices?"
python -m app.query "What is TCP/IP protocol?"
python -m app.query "What are the steps of service composition?"
```

---

## 🧠 6. Permanent Memory Trick (The Analogy)

### 🗃️ The Library Index Card Analogy:
> Think of a massive university library:
> * **`app/index.py`** is the librarian filing 1,173 detailed index cards into wooden catalog drawers.
> * **`app/query.py`** is you walking up to the catalog drawers with a magnifying glass. Before you write your final essay, you pull out the 5 closest cards to check if they actually contain the facts you need.
> * **`similarity_score`** is the percentage of overlap between what you wrote on your notepad and what is printed on the library card.

---

## 🎓 7. Senior Interview Battle Card for `query.py`

#### Q1: "Why do you inspect `similarity_search_with_score` instead of standard `similarity_search` during RAG evaluation?"
> **Senior Answer:**  
> *"Standard `similarity_search` returns documents blindly without transparency into confidence levels. By using `similarity_search_with_score`, we can inspect the exact cosine similarity score. This enables us to determine whether retrieval failures are caused by poor query formulation, low-ranking chunks, or score dilution, and allows us to establish empirical score thresholds (e.g., discarding chunks below 0.55) to prevent hallucinations."*

#### Q2: "What is the difference between Cosine Distance and Cosine Similarity?"
> **Senior Answer:**  
> *"Cosine Similarity measures the orientation angle between two vectors on a scale from -1 to +1 (or 0 to 1 for normalized non-negative embeddings), where 1 means identical direction. Cosine Distance is simply `1 - Cosine Similarity`. In similarity search, higher similarity is better, whereas in distance metrics, smaller distance indicates closer neighbors."*

#### Q3: "What is the trade-off of increasing `k` from 2 to 10?"
> **Senior Answer:**  
> *"Increasing $k$ improves **Recall**—it ensures needle-in-a-haystack items (like diluted glossary entries) are captured in the context. However, the trade-off is **Context Stuffing**: higher $k$ consumes more LLM context window tokens, marginally increases generation latency, and risks the 'Lost in the Middle' phenomenon where the LLM overlooks information buried in the middle of a large prompt."*

---

### 🏁 `app/query.py` Summary Checklist:
- [x] Know why standalone retrieval testing is essential before LLM generation.
- [x] Understand `from_existing_collection` for read-only vector querying.
- [x] Master the Symmetric Embedding rule (Query model must match Index model).
- [x] Understand Cosine Similarity scores ($0.0$ to $1.0$).
- [x] Explain the Recall vs. Context Stuffing trade-off of the $k$ parameter.
