from fastapi import APIRouter

from backend.app.core.config import get_settings

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {"ok": True}


@router.get("/version")
def version_info() -> dict:
    settings = get_settings()
    return {"name": settings.name, "version": settings.version}
