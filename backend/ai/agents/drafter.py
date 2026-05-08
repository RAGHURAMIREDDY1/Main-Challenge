import structlog
import json
from typing import List, Dict, Any
from backend.schemas.trip import Activity
from backend.ai.agents.critic import CriticAgent
from backend.services.google_maps import maps_service
from backend.core.config import get_settings
from google import genai
from google.genai import types
from pydantic import BaseModel

logger = structlog.get_logger()

from backend.schemas.trip import Activity, DecisionLogEntry, DecisionScores, DecisionRationale

class ItineraryOutput(BaseModel):
    activities: list[Activity]
    reasoning: str
    decision_log: list[DecisionLogEntry]
    efficiency_score: float

class DrafterAgent:
    """
    The Drafting Agent uses Gemini to generate the initial itinerary.
    Includes the Reflection loop using structured JSON outputs.
    """
    def __init__(self):
        self.critic = CriticAgent()
        settings = get_settings()
        self.api_key = settings.GEMINI_API_KEY
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None
            logger.warning("GEMINI_API_KEY is not set. Falling back to mock generation.")
            
    async def _call_llm(self, prompt: str) -> ItineraryOutput:
        """Abstracted LLM call demonstrating structured JSON parsing with Gemini."""
        if not self.client:
            # Fallback mock for testing without API keys
            return ItineraryOutput(
                reasoning="Prioritized indoor museum in the morning due to expected rain.",
                efficiency_score=85.0,
                decision_log=[
                    DecisionLogEntry(
                        action="Rerouted",
                        rationale="Morning rain forecast for Paris.",
                        confidence=0.95,
                        tradeoff="Missing early morning sunrise at Eiffel Tower.",
                        impact="Saved 45 minutes of potential rain delay."
                    )
                ],
                activities=[
                    Activity(
                        name="Louvre Museum", 
                        start_time="09:00", 
                        end_time="12:00", 
                        estimated_cost=20,
                        scores=DecisionScores(confidence=0.98, budget_fit=0.9, weather_suitability=1.0, efficiency=0.85, preference_match=0.95),
                        rationale=DecisionRationale(
                            selection_why="World-class indoor cultural site; perfect for rain mitigation.",
                            optimization_logic="Placed in morning slot to bypass afternoon tourist peak.",
                            alternatives_rejected="Skipped Jardin des Tuileries due to high rain probability.",
                            timing_rationale="3-hour block allows for major wing coverage without fatigue."
                        )
                    ),
                    Activity(
                        name="Bistro Lunch", 
                        start_time="12:30", 
                        end_time="14:00", 
                        estimated_cost=30,
                        scores=DecisionScores(confidence=0.92, budget_fit=0.8, weather_suitability=1.0, efficiency=0.95, preference_match=0.88),
                        rationale=DecisionRationale(
                            selection_why="Proximity to Louvre minimizes travel friction.",
                            optimization_logic="Walking distance transit (5 mins).",
                            alternatives_rejected="Rejected distant Michelin star option to preserve energy.",
                            timing_rationale="Standard Parisian lunch window."
                        )
                    )
                ]
            )

        logger.debug("calling_gemini_for_draft")
        response = self.client.models.generate_content(
            model='gemini-2.0-flash', # Updated to 2.0 as it is standard now
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ItineraryOutput,
            ),
        )
        data = json.loads(response.text)
        return ItineraryOutput(**data)

    async def generate_and_refine(self, context: Dict[str, Any], max_iterations: int = 3) -> Dict[str, Any]:
        """
        Implements the Reflection Loop (Draft -> Critic -> Refine).
        """
        logger.info("drafter_generation_started", context=context)
        
        # Inject Google Maps Context into Prompt
        destination = context.get("destination", "Paris")
        vibes = context.get("vibes", [])
        
        # Search for a relevant place dynamically to prove Maps integration
        poi_context = ""
        sample_query = f"top {vibes[0] if vibes else 'tourist'} attraction in {destination}"
        place = maps_service.search_place(sample_query)
        if place:
            poi_context = f"Google Maps Context: Consider including '{place['name']}' (Rating: {place['rating']}). "
        
        prompt = f"""
        You are an Advanced AI Travel Decision Engine. 
        Create an adaptive itinerary based on these constraints: {json.dumps(context)}
        {poi_context}
        
        Requirements for every Activity:
        1. Multi-dimensional scores (0.0 - 1.0) for: confidence, budget_fit, weather_suitability, efficiency, and preference_match.
        2. Detailed DecisionRationale explaining:
           - why this specific location was selected.
           - how the timing was optimized.
           - which specific alternatives were rejected and why.
           - why the specific start/end times were chosen.
        
        Requirements for the overall Trip:
        1. A comprehensive DecisionLogEntry for major planning pivots.
        2. realistic transit times via Google Maps logic.
        3. An overall efficiency score (0-100).
        """
        
        output = await self._call_llm(prompt)
        draft = output.activities
        reasoning = output.reasoning
        decision_log = output.decision_log
        efficiency_score = output.efficiency_score
        
        # 2. Reflection Loop
        for iteration in range(max_iterations):
            feedback = self.critic.evaluate_draft(draft, context)
            
            if feedback["is_valid"]:
                logger.info("draft_approved", iteration=iteration)
                return {
                    "activities": draft, 
                    "reasoning": reasoning, 
                    "decision_log": decision_log,
                    "efficiency_score": efficiency_score
                }
                
            logger.info("draft_rejected_refining", iteration=iteration, errors=feedback["errors"])
            
            # 3. Refinement: Provide explicit error feedback to the LLM
            refinement_prompt = f"""
            The previous draft failed strict validation. 
            Errors: {feedback['errors']}. 
            Please fix and provide an updated DecisionLogEntry for the fix.
            Original constraints: {json.dumps(context)}
            """
            
            if self.client:
                output = await self._call_llm(refinement_prompt)
                draft = output.activities
                reasoning = output.reasoning
                decision_log = output.decision_log
                efficiency_score = output.efficiency_score
            else:
                # Mock escape
                break
            
        logger.warning("max_refinements_reached_returning_best_effort")
        return {
            "activities": draft, 
            "reasoning": reasoning, 
            "decision_log": decision_log,
            "efficiency_score": efficiency_score
        }
