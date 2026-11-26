from fastapi import FastAPI
from app.routes.query_routes import router as query_router

app = FastAPI(
    title="RAG API",
    description="This is a RAG API",
    version="1.0.0"
)

app.include_router(query_router)