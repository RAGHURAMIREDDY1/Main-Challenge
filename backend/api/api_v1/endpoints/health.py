from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check() -> dict:
    """Standard health check endpoint for load balancers and Cloud Run."""
    return {"status": "healthy", "version": "1.0.0"}
