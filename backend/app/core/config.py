from functools import lru_cache
import logging
from typing import Any, Dict, List

from pydantic import BaseSettings, Field, ValidationError

logger = logging.getLogger(__name__)


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    app_name: str = Field(..., env="APP_NAME")
    app_version: str = Field(..., env="APP_VERSION")
    env: str = Field(..., env="ENV")
    debug: bool = Field(False, env="DEBUG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def name(self) -> str:
        return self.app_name

    @property
    def version(self) -> str:
        return self.app_version

    def safe_log_dict(self) -> Dict[str, Any]:
        """Return a sanitized dictionary suitable for logging."""

        return {
            "app_name": self.app_name,
            "app_version": self.app_version,
            "env": self.env,
            "debug": self.debug,
        }


@lru_cache
def get_settings() -> Settings:
    try:
        return Settings()
    except ValidationError as exc:  # pragma: no cover - startup guard
        missing_fields: List[str] = [
            error["loc"][0]
            for error in exc.errors()
            if error.get("type") == "value_error.missing"
        ]
        if missing_fields:
            message = f"Missing required environment variables: {', '.join(missing_fields)}"
        else:
            message = "Invalid configuration provided."
        logger.error(message)
        raise RuntimeError(message) from exc
