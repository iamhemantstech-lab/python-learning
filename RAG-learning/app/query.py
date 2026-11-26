"""
🛠️ DEVELOPER DIAGNOSTIC & TESTING TOOL (Local CLI Only)
=====================================================
Purpose:
  - This file is an OPTIONAL local testing tool for developers.
  - It tests ONLY the "R" (Retrieval) stage of RAG directly in your terminal.
  - It connects to Qdrant, searches for chunks, and prints cosine similarity scores.

Note for Production:
  - The actual production web application runs via:
      main.py  -->  app/routes/query_routes.py  (FastAPI + Qdrant + Gemini)
  - You do NOT need this file to run the FastAPI server or Swagger UI.
"""

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
