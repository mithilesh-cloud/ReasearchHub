from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "ResearchHub API"
    app_version: str = "0.1.0"
    api_prefix: str = "/api/v1"

    database_url: str = Field(
        default="sqlite:///./researchhub.db",
        description="SQLAlchemy database URL",
    )
    secret_key: str = Field(default="change-me", min_length=8)
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
