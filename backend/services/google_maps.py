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
        Searches for a place using the Places API and returns deep contextual data.
        """
        if not self.client:
            return {"name": query, "rating": 4.5, "address": "123 Mock St", "is_open_now": True}
            
        try:
            places_result = self.client.places(query=query)
            if not places_result.get('results'):
                return None
                
            place = places_result['results'][0]
            # Fetch Place Details for deeper intelligence (Opening hours, price, etc)
            details = self.client.place(place_id=place['place_id'], fields=['rating', 'user_ratings_total', 'opening_hours', 'price_level'])
            
            return {
                "name": place.get("name"),
                "address": place.get("formatted_address"),
                "rating": place.get("rating"),
                "price_level": details.get('result', {}).get('price_level'),
                "is_open_now": details.get('result', {}).get('opening_hours', {}).get('open_now'),
                "place_id": place.get("place_id"),
                "types": place.get("types", [])
            }
        except Exception as e:
            logger.error(f"Failed to search place: {str(e)}")
            return None

    def calculate_itinerary_efficiency(self, activities: list) -> Dict[str, Any]:
        """
        Uses Directions API to calculate total travel time and sequence efficiency.
        """
        if not self.client or len(activities) < 2:
            return {"total_travel_time_mins": 0, "efficiency_score": 100.0}

        try:
            total_time = 0
            for i in range(len(activities) - 1):
                origin = activities[i].name
                dest = activities[i+1].name
                duration = self.get_travel_time(origin, dest)
                if duration:
                    total_time += duration
            
            # Heuristic: Lower travel time relative to activity count = higher efficiency
            # Assuming 20 mins average transit is 'normal' (100%)
            avg_transit = total_time / (len(activities) - 1)
            efficiency = max(0, min(100, 120 - (avg_transit * 2)))
            
            return {
                "total_travel_time_mins": total_time,
                "efficiency_score": round(efficiency, 1)
            }
        except Exception as e:
            logger.error(f"Efficiency calculation failed: {str(e)}")
            return {"total_travel_time_mins": 0, "efficiency_score": 0.0}

# Singleton instance
maps_service = GoogleMapsService()
