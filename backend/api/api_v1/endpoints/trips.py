from fastapi import APIRouter, Depends, HTTPException
from backend.schemas.trip import TripPreferences, TripResponse
from backend.services.ai_orchestrator import AIOrchestrator

router = APIRouter()

def get_orchestrator() -> AIOrchestrator:
    return AIOrchestrator()

@router.post("/generate", response_model=TripResponse)
async def generate_trip(
    prefs: TripPreferences,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
) -> TripResponse:
    """
    Endpoint to dynamically generate an AI-powered travel itinerary.
    """
    try:
        # FastAPI handles async elegantly without blocking
        return await orchestrator.generate_itinerary(prefs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
