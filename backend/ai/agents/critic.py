import structlog
from typing import List, Dict, Any
from backend.schemas.trip import Activity
from backend.services.google_maps import maps_service

logger = structlog.get_logger()

class CriticAgent:
    """
    The Validation Agent that acts as a deterministic safety net.
    It checks for schedule overlaps, transit feasibility via Google Maps, 
    budget overruns, and weather mismatches.
    """
    
    def _time_to_minutes(self, t_str: str) -> int:
        try:
            h, m = map(int, t_str.split(':'))
            return h * 60 + m
        except:
            return 0
            
    def evaluate_draft(self, draft_activities: List[Activity], constraints: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluates an itinerary draft and returns actionable feedback."""
        logger.info("critic_evaluation_started")
        feedback = {"is_valid": True, "errors": []}
        
        # Check 1: Budget
        total_cost = sum(a.estimated_cost for a in draft_activities)
        if total_cost > constraints.get("max_budget", float('inf')):
            feedback["is_valid"] = False
            feedback["errors"].append(f"Budget exceeded. Total: ${total_cost}, Max: ${constraints['max_budget']}")
            
        # Check 2: Schedule Overlaps & Transit Times (Google Maps Integration)
        for i in range(len(draft_activities) - 1):
            act_current = draft_activities[i]
            act_next = draft_activities[i+1]
            
            end_mins = self._time_to_minutes(act_current.end_time)
            start_mins = self._time_to_minutes(act_next.start_time)
            
            # Basic overlap
            if end_mins > start_mins:
                feedback["is_valid"] = False
                feedback["errors"].append(
                    f"Schedule conflict: {act_current.name} ends at {act_current.end_time}, "
                    f"but {act_next.name} starts at {act_next.start_time}."
                )
                continue
                
            # Maps Transit Check
            available_transit_time = start_mins - end_mins
            destination_city = constraints.get("destination", "")
            
            # We append destination to help Maps geocode correctly
            origin_query = f"{act_current.name}, {destination_city}"
            dest_query = f"{act_next.name}, {destination_city}"
            
            estimated_transit = maps_service.get_travel_time(origin_query, dest_query)
            
            if estimated_transit is not None:
                if estimated_transit > available_transit_time:
                    feedback["is_valid"] = False
                    feedback["errors"].append(
                        f"Transit conflict: Google Maps estimates {estimated_transit} mins transit "
                        f"between '{act_current.name}' and '{act_next.name}', but only "
                        f"{available_transit_time} mins are allocated."
                    )
                else:
                    logger.debug("transit_validated", origin=act_current.name, dest=act_next.name, est=estimated_transit)

        # Check 3: Weather (If rain and outdoor)
        weather = constraints.get("weather_forecast", "sunny").lower()
        if weather in ["rain", "storm"]:
            for act in draft_activities:
                if "park" in act.name.lower() or "beach" in act.name.lower():
                    feedback["is_valid"] = False
                    feedback["errors"].append(f"Weather conflict: {act.name} is outdoor but forecast is {weather}.")
                    
        logger.info("critic_evaluation_completed", is_valid=feedback["is_valid"], error_count=len(feedback["errors"]))
        return feedback
