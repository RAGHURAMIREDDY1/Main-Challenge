from fastapi import APIRouter
from backend.api.api_v1.endpoints import health, trips

api_router = APIRouter()

# Clean router separation
api_router.include_router(health.router, tags=["System"])
api_router.include_router(trips.router, prefix="/trips", tags=["Trips"])
