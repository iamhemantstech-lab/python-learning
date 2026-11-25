from fastapi import FastAPI
from routes import book_routes
from routes import user_routes
from database import create_tables

app = FastAPI(
    title="Book exchange API",
    description="A simple api for exchanging used books",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_tables()

app.include_router(user_routes.router)
app.include_router(book_routes.router)

@app.get("/")
def home():
    return {"message": "Welcome to book exchange API"}
