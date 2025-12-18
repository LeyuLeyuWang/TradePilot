import pytest
from fastapi.testclient import TestClient


def test_health_endpoint(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("APP_NAME", "TradePilot")
    monkeypatch.setenv("APP_VERSION", "0.0.0")
    monkeypatch.setenv("ENV", "test")

    from backend.app.main import app

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True}
