import structlog
from typing import List, Dict, Any
from backend.schemas.trip import Activity

logger = structlog.get_logger()

class CriticAgent:
    """
    The Validation Agent that acts as a deterministic safety net.
    It checks for schedule overlaps, budget overruns, and weather mismatches.
    """
    
    def evaluate_draft(self, draft_activities: List[Activity], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates an itinerary draft and returns actionable feedback."""
        logger.info("critic_evaluation_started")
        feedback = {"is_valid": True, "errors": []}
        
        # Check 1: Budget
        total_cost = sum(a.estimated_cost for a in draft_activities)
        if total_cost > constraints.get("max_budget", float('inf')):
            feedback["is_valid"] = False
            feedback["errors"].append(f"Budget exceeded. Total: ${total_cost}, Max: ${constraints['max_budget']}")
            
        # Check 2: Schedule Overlaps (Simplified)
        # Assuming sorted by start_time
        for i in range(len(draft_activities) - 1):
            if draft_activities[i].end_time > draft_activities[i+1].start_time:
                feedback["is_valid"] = False
                feedback["errors"].append(
                    f"Schedule conflict between {draft_activities[i].name} and {draft_activities[i+1].name}"
                )
                
        # Check 3: Weather (If rain and outdoor)
        weather = constraints.get("weather_forecast", "sunny").lower()
        if weather in ["rain", "storm"]:
            for act in draft_activities:
                # Simulating metadata check
                if "park" in act.name.lower() or "beach" in act.name.lower():
                    feedback["is_valid"] = False
                    feedback["errors"].append(f"Weather conflict: {act.name} is outdoor but forecast is {weather}.")
                    
        logger.info("critic_evaluation_completed", is_valid=feedback["is_valid"], error_count=len(feedback["errors"]))
        return feedback
