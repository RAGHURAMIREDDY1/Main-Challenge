import structlog
import uuid
from tenacity import retry, stop_after_attempt, wait_exponential
from backend.schemas.trip import TripPreferences, TripResponse, Activity
from backend.services.weather import WeatherService
from backend.services.budget import BudgetOptimizer
from backend.services.optimization_engine import OptimizationEngine
from backend.ai.agents.drafter import DrafterAgent

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
        self.drafter = DrafterAgent()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_itinerary(self, prefs: TripPreferences) -> TripResponse:
        """
        Orchestrates the AI planning workflow.
        Uses tenacity for automatic retries to handle transient LLM failures.
        """
        logger.info("orchestration_started", destination=prefs.destination)
        
        # 1. Fetch Context
        forecast = await self.weather.get_forecast(prefs.destination, prefs.start_date)
        
        # 2. Contextual Data for Drafter
        context = {
            "destination": prefs.destination,
            "max_budget": prefs.budget_usd,
            "vibes": prefs.vibes,
            "weather_forecast": forecast
        }
        
        # 3. Drafter AI Generation & Critic Verification
        draft_response = await self.drafter.generate_and_refine(context)
        draft_activities = draft_response["activities"]
        ai_reasoning = draft_response["reasoning"]
        
        # 4. Optimize & Resolve Conflicts
        optimized_activities = self.optimizer.resolve_conflicts(draft_activities)
        
        # 5. Validate Budget
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
            ai_reasoning=ai_reasoning
        )
