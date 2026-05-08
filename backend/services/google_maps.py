import googlemaps
from typing import Dict, Any, Optional
import structlog
from backend.core.config import get_settings

logger = structlog.get_logger(__name__)

class GoogleMapsService:
    def __init__(self):
        settings = get_settings()
        self.api_key = settings.GOOGLE_MAPS_API_KEY
        if not self.api_key:
            logger.warning("GOOGLE_MAPS_API_KEY is not set. Google Maps integrations will be bypassed.")
            self.client = None
        else:
            self.client = googlemaps.Client(key=self.api_key)

    def get_travel_time(self, origin: str, destination: str, mode: str = "transit") -> Optional[int]:
        """
        Calculates the travel time between two locations in minutes.
        Uses Directions API.
        """
        if not self.client:
            return 30  # Fallback dummy value
            
        try:
            directions = self.client.directions(
                origin,
                destination,
                mode=mode,
                departure_time="now"
            )
            if not directions:
                return None
            
            leg = directions[0]['legs'][0]
            duration_mins = int(leg['duration']['value'] / 60)
            return duration_mins
        except Exception as e:
            logger.error(f"Failed to fetch directions: {str(e)}")
            return None

    def search_place(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Searches for a place using the Places API and returns its details.
        """
        if not self.client:
            return {"name": query, "rating": 4.5, "address": "123 Mock St"}
            
        try:
            places_result = self.client.places(query=query)
            if not places_result.get('results'):
                return None
                
            place = places_result['results'][0]
            return {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating"),
                "place_id": place.get("place_id"),
                "types": place.get("types", [])
            }
        except Exception as e:
            logger.error(f"Failed to search place: {str(e)}")
            return None

# Singleton instance
maps_service = GoogleMapsService()
