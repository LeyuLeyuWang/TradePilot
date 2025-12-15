from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    name: str = "TradePilot"
    version: str = "0.1.0"

    class Config:
        env_prefix = "APP_"
        case_sensitive = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
