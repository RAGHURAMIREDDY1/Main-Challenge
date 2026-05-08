import structlog
from typing import List, Dict, Any
from backend.schemas.trip import Activity, DecisionLogEntry
from backend.ai.agents.drafter import DrafterAgent

logger = structlog.get_logger()

class AdaptationService:
    """
    Handles real-time disruptions and triggers intelligent re-planning.
    Acts as the 'Operations' layer of the platform.
    """
    def __init__(self):
        self.drafter = DrafterAgent()

    async def handle_disruption(self, current_itinerary: List[Activity], event_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Takes a current itinerary and an event (e.g., 'Heavy Rain', 'Budget Cut') 
        and returns a rerouted/adapted version.
        """
        logger.info("disruption_detected", event_type=event_type)
        
        # We enrich the context with the disruption event
        context["disruption_event"] = event_type
        context["current_itinerary"] = [a.dict() for a in current_itinerary]
        
        # Re-trigger the Drafter with the new context
        # The Drafter is already designed to handle constraints and output reasoning
        adaptation_result = await self.drafter.generate_and_refine(context)
        
        # We can add an 'Adaptation' specific log entry here to ensure visibility
        adaptation_result["decision_log"].insert(0, DecisionLogEntry(
            action="Adapted Plan",
            rationale=f"Detected {event_type}. Triggered real-time itinerary optimization.",
            confidence=0.98,
            tradeoff="Modified original sequence to handle environment change.",
            impact="Maintained trip continuity despite disruption."
        ))
        
        return adaptation_result
