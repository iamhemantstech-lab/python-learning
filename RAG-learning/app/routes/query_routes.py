import os
from pathlib import Path
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_qdrant import QdrantVectorStore
from google import genai

# Robust .env loading: ensures .env is found whether running from root or RAG-learning folder
_base_dir = Path(__file__).resolve().parent  # app/routes
_rag_env = _base_dir.parent.parent / ".env"  # RAG-learning/.env
_app_env = _base_dir.parent / ".env"         # RAG-learning/app/.env
_root_env = _base_dir.parent.parent.parent / ".env"  # hemant-python/.env

for env_file in [_rag_env, _app_env, _root_env]:
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=True)
load_dotenv(override=True)

router = APIRouter(
    prefix="/query",
    tags=["query"],
)

# 1. Free Local Embedding Model (384 dimensions - matches index.py)
embedding_model = FastEmbedEmbeddings(model_name="BAAI/bge-small-en-v1.5")

# 2. Connect to existing Qdrant collection
vector_db = QdrantVectorStore.from_existing_collection(
    embedding=embedding_model,
    collection_name="sample_collection",
    url="http://localhost:6333",
)


# Pydantic schemas for request and response
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


def get_gemini_api_key() -> str:
    """Dynamically get the GEMINI_API_KEY, reloading .env if needed."""
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        for env_file in [_rag_env, _app_env, _root_env]:
            if env_file.exists():
                load_dotenv(dotenv_path=env_file, override=True)
        key = os.getenv("GEMINI_API_KEY", "").strip()
    return key


@router.post("/", response_model=QueryResponse)
async def query(request: QueryRequest):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty.")

    # Step 1: Retrieval (R) - Local Similarity Search with FastEmbed
    search_results = vector_db.similarity_search_with_score(query=question, k=10)

    if not search_results:
        return QueryResponse(
            question=question,
            answer="No relevant documents found in the database.",
            sources=[],
        )

    # Format retrieved sources
    sources = [
        SourceChunk(
            page=doc.metadata.get("page", 0) + 1,
            similarity_score=round(float(score), 4),
            content=doc.page_content.strip(),
        )
        for doc, score in search_results
    ]

    # Step 2: Augmentation (A) - Assemble Context
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

    # Step 3: Generation (G) - Free Google Gemini API
    gemini_key = get_gemini_api_key()

    if gemini_key:
        try:
            client = genai.Client(api_key=gemini_key)
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )
            answer = response.text.strip()
        except Exception as e:
            answer = (
                f"[Retrieved Context from Page {sources[0].page}]:\n\n"
                f"{sources[0].content}\n\n"
                f"(Note: Gemini LLM call failed: {e})"
            )
    else:
        answer = (
            f"[Context retrieved from Page {sources[0].page}]:\n\n"
            f"{sources[0].content}\n\n"
            f"💡 Tip: Add your GEMINI_API_KEY to .env to generate AI answers automatically!"
        )

    return QueryResponse(
        question=question,
        answer=answer,
        sources=sources,
    )
