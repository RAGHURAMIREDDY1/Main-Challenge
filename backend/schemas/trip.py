from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

class TripPreferences(BaseModel):
    """User preferences for generating a trip."""
    destination: str = Field(..., description="Target city or country")
    start_date: date = Field(..., description="Start date of the trip")
    end_date: date = Field(..., description="End date of the trip")
    budget_usd: float = Field(..., gt=0, description="Total budget in USD")
    vibes: List[str] = Field(default_factory=list, description="Preferred styles, e.g., ['chill', 'foodie']")

class DecisionScores(BaseModel):
    """Multi-dimensional scoring for an AI decision."""
    confidence: float = Field(..., ge=0, le=1.0)
    budget_fit: float = Field(..., ge=0, le=1.0)
    weather_suitability: float = Field(..., ge=0, le=1.0)
    efficiency: float = Field(..., ge=0, le=1.0)
    preference_match: float = Field(..., ge=0, le=1.0)

class DecisionRationale(BaseModel):
    """Detailed explanation of the AI's logic."""
    selection_why: str
    optimization_logic: str
    alternatives_rejected: str
    timing_rationale: str

class Activity(BaseModel):
    """A single activity with its associated decision metadata."""
    name: str = Field(..., description="Name of the activity or POI")
    start_time: str = Field(..., description="Expected start time (HH:MM)")
    end_time: str = Field(..., description="Expected end time (HH:MM)")
    estimated_cost: float = Field(0.0, description="Estimated cost in USD")
    description: Optional[str] = None
    scores: DecisionScores
    rationale: DecisionRationale

class DecisionLogEntry(BaseModel):
    """Represents a single intelligent decision made by the AI."""
    action: str = Field(..., description="The type of action taken (e.g., 'Rerouted', 'Substituted')")
    rationale: str = Field(..., description="The reasoning behind the decision")
    confidence: float = Field(..., ge=0, le=1.0, description="Confidence score for this decision")
    tradeoff: str = Field(..., description="What was compromised to achieve this optimization")
    impact: str = Field(..., description="The measurable benefit (e.g., 'Saved 20 minutes')")

class TripResponse(BaseModel):
    """Final optimized itinerary response with evolution tracking."""
    trip_id: str
    destination: str
    total_cost: float
    activities: List[Activity]
    evolution_history: List[List[Activity]] = Field(default_factory=list, description="Historical versions of the itinerary")
    ai_reasoning: str = Field(..., description="Overall summary of the strategy")
    decision_log: List[DecisionLogEntry] = Field(default_factory=list, description="Step-by-step logic log")
    efficiency_score: float = Field(default=0.0, description="0-100 score of route/budget efficiency")
