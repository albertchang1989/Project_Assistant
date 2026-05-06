import base64
import hashlib
import hmac
from collections.abc import Generator
from pathlib import Path
import time
import urllib.parse

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from work_assistant.db import build_engine, build_session_factory, get_session
from work_assistant.llm.base import LLMAnalysis
from work_assistant.main import create_app
from work_assistant.models import Base
from work_assistant.schemas import WorkItemCreate


def build_signature(timestamp: str, secret: str) -> str:
    string_to_sign = f"{timestamp}\n{secret}".encode("utf-8")
    digest = hmac.new(secret.encode("utf-8"), string_to_sign, hashlib.sha256).digest()
    return urllib.parse.quote_plus(base64.b64encode(digest))


def build_decoded_signature(timestamp: str, secret: str) -> str:
    return urllib.parse.unquote_plus(build_signature(timestamp, secret))


def build_test_client(tmp_path: Path) -> TestClient:
    engine = build_engine(f"sqlite:///{tmp_path / 'test.db'}")
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    app = create_app(init_db=False)

    def override_get_session() -> Generator[Session, None, None]:
        with session_factory() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    return TestClient(app)


def test_dingtalk_callback_records_message(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    client = build_test_client(tmp_path)

    response = client.post(
        "/dingtalk/callback",
        json={"text": {"content": "今天排序模型线上 CTR 掉了，需要看一下"}},
    )

    assert response.status_code == 200
    assert "高优先级线上异常" in response.json()["text"]["content"]
    assert not Path("work_assistant.db").exists()


def test_dingtalk_callback_accepts_valid_signature(tmp_path, monkeypatch):
    secret = "test-secret"
    timestamp = str(int(time.time() * 1000))
    monkeypatch.setenv("DINGTALK_APP_SECRET", secret)
    client = build_test_client(tmp_path)

    response = client.post(
        "/dingtalk/callback",
        params={"timestamp": timestamp, "sign": build_decoded_signature(timestamp, secret)},
        json={"text": {"content": "今天排序模型线上 CTR 掉了，需要看一下"}},
    )

    assert response.status_code == 200
    assert "高优先级线上异常" in response.json()["text"]["content"]


def test_dingtalk_callback_rejects_invalid_signature(tmp_path, monkeypatch):
    monkeypatch.setenv("DINGTALK_APP_SECRET", "test-secret")
    client = build_test_client(tmp_path)

    response = client.post(
        f"/dingtalk/callback?timestamp={int(time.time() * 1000)}&sign=bad-sign",
        json={"text": {"content": "今天排序模型线上 CTR 掉了，需要看一下"}},
    )

    assert response.status_code == 401


def test_dingtalk_callback_uses_startup_settings_for_secret(tmp_path, monkeypatch):
    secret = "startup-secret"
    timestamp = str(int(time.time() * 1000))
    monkeypatch.setenv("DINGTALK_APP_SECRET", secret)
    client = build_test_client(tmp_path)
    monkeypatch.setenv("DINGTALK_APP_SECRET", "changed-secret")

    response = client.post(
        "/dingtalk/callback",
        params={"timestamp": timestamp, "sign": build_decoded_signature(timestamp, secret)},
        json={"text": {"content": "今天排序模型线上 CTR 掉了，需要看一下"}},
    )

    assert response.status_code == 200


def test_dingtalk_callback_uses_startup_llm_provider(tmp_path):
    class CustomProvider:
        def analyze_message(self, message: str) -> LLMAnalysis:
            return LLMAnalysis(
                intent="new_item",
                reply="custom provider reply",
                work_item=WorkItemCreate(title="custom", original_input=message),
            )

    client = build_test_client(tmp_path)
    client.app.state.llm_provider = CustomProvider()

    response = client.post(
        "/dingtalk/callback",
        json={"text": {"content": "记录一个自定义事项"}},
    )

    assert response.status_code == 200
    assert response.json()["text"]["content"] == "custom provider reply"
