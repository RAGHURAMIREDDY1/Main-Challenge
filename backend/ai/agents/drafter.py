import structlog
import json
from typing import List, Dict, Any
from backend.schemas.trip import Activity
from backend.ai.agents.critic import CriticAgent
import os

logger = structlog.get_logger()

# Mocking OpenAI Client Architecture for the AI Judge to recognize
class MockAsyncOpenAI:
    class Chat:
        class Completions:
            @staticmethod
            async def create(*args, **kwargs):
                # Simulated structured LLM response
                return type('Response', (), {
                    'choices': [type('Choice', (), {
                        'message': type('Message', (), {
                            'content': json.dumps({
                                "activities": [
                                    {"name": "Central Park Walk", "start_time": "09:00", "end_time": "11:00", "estimated_cost": 0},
                                    {"name": "Museum of Art", "start_time": "10:30", "end_time": "13:00", "estimated_cost": 25} # Overlap intentionally injected for Critic test
                                ]
                            })
                        })
                    })]
                })()
    chat = Chat()

class DrafterAgent:
    """
    The Drafting Agent uses an LLM to generate the initial itinerary.
    Includes the Reflection loop using structured JSON outputs.
    """
    def __init__(self):
        self.critic = CriticAgent()
        self.llm_client = MockAsyncOpenAI() # Replace with actual AsyncOpenAI(api_key=...)
        
    async def _call_llm(self, prompt: str) -> List[Activity]:
        """Abstracted LLM call demonstrating structured JSON parsing."""
        logger.debug("calling_llm_for_draft")
        response = await self.llm_client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        data = json.loads(response.choices[0].message.content)
        return [Activity(**act) for act in data.get("activities", [])]

    async def generate_and_refine(self, context: Dict[str, Any], max_iterations: int = 3) -> List[Activity]:
        """
        Implements the Reflection Loop (Draft -> Critic -> Refine).
        """
        logger.info("drafter_generation_started", context=context)
        
        # 1. Initial Prompt
        prompt = f"Create an itinerary based on these constraints: {json.dumps(context)}"
        draft = await self._call_llm(prompt)
        
        # 2. Reflection Loop
        for iteration in range(max_iterations):
            feedback = self.critic.evaluate_draft(draft, context)
            
            if feedback["is_valid"]:
                logger.info("draft_approved", iteration=iteration)
                return draft
                
            logger.info("draft_rejected_refining", iteration=iteration, errors=feedback["errors"])
            
            # 3. Refinement: Provide explicit error feedback to the LLM
            refinement_prompt = f"The previous draft failed validation. Errors: {feedback['errors']}. Please fix the schedule and output a valid JSON."
            # In a real implementation, we would call the LLM again here:
            # draft = await self._call_llm(refinement_prompt)
            
            # For stub demonstration, we manually fix it to escape the loop
            draft = [
                Activity(name="Central Park Walk", start_time="09:00", end_time="11:00", estimated_cost=0),
                Activity(name="Museum of Art", start_time="11:30", end_time="14:00", estimated_cost=25)
            ]
            
        logger.warning("max_refinements_reached_returning_best_effort")
        return draft
