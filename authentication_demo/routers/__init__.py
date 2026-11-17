from fastapi import APIRouter
from .auth_route import router as auth_router
from .users_route import router as users_router

# Master API Router with standard /api/v1 prefix
api_router = APIRouter(prefix="/api/v1")

# public routes
api_router.include_router(auth_router)

# protected routes
api_router.include_router(users_router)