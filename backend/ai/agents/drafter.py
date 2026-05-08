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

class ItineraryOutput(BaseModel):
    activities: list[Activity]
    reasoning: str

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
                reasoning="Mock reasoning due to missing API key.",
                activities=[
                    Activity(name="Central Park Walk", start_time="09:00", end_time="11:00", estimated_cost=0),
                    Activity(name="Museum of Art", start_time="11:30", end_time="14:00", estimated_cost=25)
                ]
            )

        logger.debug("calling_gemini_for_draft")
        response = self.client.models.generate_content(
            model='gemini-2.5-flash',
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
        You are an expert AI Travel Agent. Create an itinerary based on these constraints: {json.dumps(context)}
        {poi_context}
        Output a detailed timeline. Ensure transit times are realistic.
        """
        
        output = await self._call_llm(prompt)
        draft = output.activities
        reasoning = output.reasoning
        
        # 2. Reflection Loop
        for iteration in range(max_iterations):
            feedback = self.critic.evaluate_draft(draft, context)
            
            if feedback["is_valid"]:
                logger.info("draft_approved", iteration=iteration)
                return {"activities": draft, "reasoning": reasoning}
                
            logger.info("draft_rejected_refining", iteration=iteration, errors=feedback["errors"])
            
            # 3. Refinement: Provide explicit error feedback to the LLM
            refinement_prompt = f"""
            The previous draft failed strict transit/budget validation. 
            Errors: {feedback['errors']}. 
            Please fix the schedule. Ensure walking/transit times are realistic between locations.
            Original constraints: {json.dumps(context)}
            """
            
            if self.client:
                output = await self._call_llm(refinement_prompt)
                draft = output.activities
                reasoning = output.reasoning
            else:
                # Mock escape
                break
            
        logger.warning("max_refinements_reached_returning_best_effort")
        return {"activities": draft, "reasoning": reasoning}
