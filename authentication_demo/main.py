# Starts FastAPI application
from fastapi import FastAPI
from database import engine, Base
from models import User
from routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Authentication System",
    description="User Authentication using FastAPI and MySQL",
    version="1.0.0"
)

app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Authentication API is running"}

@app.get("/health")
def health_check():
    return {"message": "API is running"}

@app.get("/about")
def about():
    return {
        "project": "User Authentication System",
        "backend": "FastAPI",
        "database": "MySQL"
    }