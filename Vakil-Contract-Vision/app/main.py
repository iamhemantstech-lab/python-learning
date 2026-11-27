from fastapi import FastAPI
from database import init_db
from routes.contracts_routes import router as contract_route
from routes.analysis_routes import router as analysis_route

app = FastAPI(
    title="Vakil Contracts API",
    description="AI-Powered Contract Analysis using Gemini",
    version="1.0.0"
)

@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(contract_route)
app.include_router(analysis_route)

@app.get("/")
async def root():
    return {
        "message": "Vakil Contrats API is running."
    }

