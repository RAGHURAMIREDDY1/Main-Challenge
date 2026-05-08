import structlog
from typing import Dict, Any

logger = structlog.get_logger()

class ScoringEngine:
    """
    Implements the Dynamic Recommendation Scoring Logic.
    Score = (Semantic_Match * 0.5) + (Weather_Suitability * 0.3) + (Budget_Alignment * 0.2)
    """
    def __init__(self, weights: Dict[str, float] = None):
        self.weights = weights or {
            "semantic": 0.5,
            "weather": 0.3,
            "budget": 0.2
        }

    def calculate_score(self, poi: Dict[str, Any], user_vibe_score: float, weather_condition: str, remaining_budget: float) -> float:
        """Calculates the composite score for a Point of Interest (POI)."""
        # 1. Semantic Match (Simulated)
        semantic_score = user_vibe_score * self.weights["semantic"]
        
        # 2. Weather Suitability
        weather_score = 1.0
        if weather_condition.lower() in ["rain", "storm"] and poi.get("is_outdoor", False):
            weather_score = 0.1 # Heavy penalty for outdoor activities in bad weather
            logger.debug("weather_penalty_applied", poi=poi["name"])
        weather_score *= self.weights["weather"]
        
        # 3. Budget Alignment
        budget_score = 1.0
        cost = poi.get("estimated_cost", 0)
        if cost > (remaining_budget * 0.5):
            budget_score = 0.2 # Penalty if it takes up too much of the remaining budget
        budget_score *= self.weights["budget"]
        
        final_score = semantic_score + weather_score + budget_score
        return round(final_score, 2)
