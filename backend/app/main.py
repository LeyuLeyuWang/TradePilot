import logging

from fastapi import FastAPI

from backend.app.api.routes.health import router as health_router
from backend.app.core.config import get_settings

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(title=settings.name, version=settings.version)
    app.include_router(health_router)

    @app.on_event("startup")
    async def log_startup() -> None:
        logger.info("Settings loaded successfully")
        logger.info(
            "Startup configuration: %s",
            settings.safe_log_dict(),
        )

    return app


app = create_app()
