from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Scrapify AI"
    debug: bool = False

    # OpenAI API settings
    openai_default_model: str = "gpt-4o"  # Default model
    
    # Serper API settings
    serper_api_key: str = ""
    proxycurl_api_key: str = ""

    class Config:
        env_file = ".env"
        extra = "ignore"  # Optional: allows extra fields without validation errors


@lru_cache()
def get_settings():
    return Settings()
