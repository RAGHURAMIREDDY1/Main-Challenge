from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """
    Centralized configuration management.
    Reads from environment variables and provides strict typing.
    """
    PROJECT_NAME: str = "AI Travel Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment
    ENVIRONMENT: str = "development"
    
    # External APIs
    OPENAI_API_KEY: str | None = None
    WEATHER_API_KEY: str | None = None
    
    # Database
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/travel_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

@lru_cache()
def get_settings() -> Settings:
    """Returns a cached instance of the settings."""
    return Settings()
