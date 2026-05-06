import pytest
from fastapi.testclient import TestClient

from work_assistant.main import create_app


def test_health_check_returns_ok():
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_app_rejects_missing_dingtalk_secret_in_production(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.delenv("DINGTALK_APP_SECRET", raising=False)

    with pytest.raises(ValueError, match="DINGTALK_APP_SECRET"):
        create_app(init_db=False)


def test_create_app_starts_scheduler_in_production(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("DINGTALK_APP_SECRET", "test-secret")
    monkeypatch.setenv("DINGTALK_OUTGOING_WEBHOOK", "https://example.test/webhook")

    app = create_app(init_db=False)

    try:
        assert app.state.scheduler.running is True
    finally:
        app.state.scheduler.shutdown()
