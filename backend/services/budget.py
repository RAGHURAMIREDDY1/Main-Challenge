import structlog
from backend.schemas.trip import Activity
from typing import List

logger = structlog.get_logger()

class BudgetOptimizer:
    """Handles logic for keeping the itinerary within budget."""
    
    def calculate_total(self, activities: List[Activity]) -> float:
        return sum(activity.estimated_cost for activity in activities)
    
    def validate_budget(self, activities: List[Activity], max_budget: float) -> bool:
        """Returns True if the total cost is within the max_budget."""
        total = self.calculate_total(activities)
        is_valid = total <= max_budget
        if not is_valid:
            logger.warning("budget_exceeded", total=total, max_budget=max_budget)
        return is_valid
