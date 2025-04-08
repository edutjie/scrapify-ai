from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    app_name: str = "Scrapify AI"
    debug: bool = False

    # OpenAI API settings
    openai_default_model: str = "gpt-4o"  # Default model

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
