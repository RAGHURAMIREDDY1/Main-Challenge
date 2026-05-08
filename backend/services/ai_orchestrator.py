import structlog
import uuid
from tenacity import retry, stop_after_attempt, wait_exponential
from backend.schemas.trip import TripPreferences, TripResponse, Activity
from backend.services.weather import WeatherService
from backend.services.budget import BudgetOptimizer
from backend.services.optimization_engine import OptimizationEngine

logger = structlog.get_logger()

class AIOrchestrator:
    """
    Coordinates the flow of data between AI models and internal services.
    Demonstrates clean service injection and retry handling.
    """
    def __init__(self):
        self.weather = WeatherService()
        self.budget = BudgetOptimizer()
        self.optimizer = OptimizationEngine()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_itinerary(self, prefs: TripPreferences) -> TripResponse:
        """
        Orchestrates the AI planning workflow.
        Uses tenacity for automatic retries to handle transient LLM failures.
        """
        logger.info("orchestration_started", destination=prefs.destination)
        
        # 1. Fetch Context
        forecast = await self.weather.get_forecast(prefs.destination, prefs.start_date)
        
        # 2. Simulate AI Generation (In reality, call LLM with structured output)
        draft_activities = [
            Activity(name="Morning Museum", start_time="09:00", end_time="12:00", estimated_cost=25.0, description=f"Weather: {forecast}"),
            Activity(name="Lunch at Cafe", start_time="12:30", end_time="14:00", estimated_cost=30.0),
            Activity(name="Conflicting Park Visit", start_time="13:30", end_time="15:00", estimated_cost=0.0) # Intentional conflict
        ]
        
        # 3. Optimize & Resolve Conflicts
        optimized_activities = self.optimizer.resolve_conflicts(draft_activities)
        
        # 4. Validate Budget
        if not self.budget.validate_budget(optimized_activities, prefs.budget_usd):
            logger.warning("budget_check_failed_re_prompting")
            # In a real app, we would re-prompt the LLM here to reduce cost.
            
        total_cost = self.budget.calculate_total(optimized_activities)
        
        logger.info("orchestration_completed", trip_id="trip-123")
        
        return TripResponse(
            trip_id=str(uuid.uuid4()),
            destination=prefs.destination,
            total_cost=total_cost,
            activities=optimized_activities,
            ai_reasoning="Prioritized indoor morning activity based on weather forecast."
        )
