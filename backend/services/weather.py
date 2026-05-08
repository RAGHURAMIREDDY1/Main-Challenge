import structlog
from datetime import date

logger = structlog.get_logger()

class WeatherService:
    """Abstraction for external weather integrations."""
    
    async def get_forecast(self, location: str, target_date: date) -> str:
        """
        Simulates fetching weather forecast.
        In production, this would call OpenWeatherMap or similar.
        """
        logger.info("fetching_weather", location=location, date=str(target_date))
        # Simulated response for hackathon stub
        return "Sunny with a chance of light rain in the afternoon."
