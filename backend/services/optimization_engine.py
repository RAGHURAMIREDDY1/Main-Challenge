import structlog
from backend.schemas.trip import Activity
from typing import List
from datetime import datetime

logger = structlog.get_logger()

class OptimizationEngine:
    """Resolves scheduling conflicts and optimizes routing."""
    
    def resolve_conflicts(self, activities: List[Activity]) -> List[Activity]:
        """
        Sorts activities by time and removes overlapping events.
        A real implementation would use constraint programming or AI.
        """
        logger.info("resolving_schedule_conflicts")
        
        def to_time(t: str) -> datetime:
            return datetime.strptime(t, "%H:%M")
            
        sorted_activities = sorted(activities, key=lambda a: to_time(a.start_time))
        valid_activities = []
        
        last_end = None
        for act in sorted_activities:
            start = to_time(act.start_time)
            if last_end is None or start >= last_end:
                valid_activities.append(act)
                last_end = to_time(act.end_time)
            else:
                logger.info("conflict_detected_and_removed", activity=act.name)
                
        return valid_activities
