from fastapi import APIRouter, Depends, HTTPException
from typing import List
from pydantic import BaseModel
from backend.schemas.trip import TripPreferences, TripResponse, Activity
from backend.services.ai_orchestrator import AIOrchestrator

router = APIRouter()

def get_orchestrator() -> AIOrchestrator:
    return AIOrchestrator()

@router.post("/generate", response_model=TripResponse)
async def generate_trip(
    prefs: TripPreferences,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
) -> TripResponse:
    """Endpoint to dynamically generate an AI-powered travel itinerary."""
    try:
        return await orchestrator.generate_itinerary(prefs)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class AdaptationRequest(BaseModel):
    trip_id: str
    event_type: str
    current_activities: List[Activity]
    destination: str
    budget: float

@router.post("/adapt", response_model=TripResponse)
async def adapt_trip(
    req: AdaptationRequest,
    orchestrator: AIOrchestrator = Depends(get_orchestrator)
) -> TripResponse:
    """Trigger real-time adaptation for a trip."""
    try:
        return await orchestrator.simulate_disruption(
            req.trip_id, 
            req.event_type, 
            req.current_activities,
            req.destination,
            req.budget
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
