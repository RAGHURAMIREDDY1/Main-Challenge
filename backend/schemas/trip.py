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

class Activity(BaseModel):
    """A single activity in the itinerary."""
    name: str = Field(..., description="Name of the activity or POI")
    start_time: str = Field(..., description="Expected start time (HH:MM)")
    end_time: str = Field(..., description="Expected end time (HH:MM)")
    estimated_cost: float = Field(0.0, description="Estimated cost in USD")
    description: Optional[str] = None

class DecisionLogEntry(BaseModel):
    """Represents a single intelligent decision made by the AI."""
    action: str = Field(..., description="The type of action taken (e.g., 'Rerouted', 'Substituted')")
    rationale: str = Field(..., description="The reasoning behind the decision")
    confidence: float = Field(..., ge=0, le=1.0, description="Confidence score for this decision")
    tradeoff: str = Field(..., description="What was compromised to achieve this optimization")
    impact: str = Field(..., description="The measurable benefit (e.g., 'Saved 20 minutes')")

class TripResponse(BaseModel):
    """Final optimized itinerary response with transparency data."""
    trip_id: str
    destination: str
    total_cost: float
    activities: List[Activity]
    ai_reasoning: str = Field(..., description="Overall summary of the strategy")
    decision_log: List[DecisionLogEntry] = Field(default_factory=list, description="Step-by-step logic log")
    efficiency_score: float = Field(default=0.0, description="0-100 score of route/budget efficiency")
