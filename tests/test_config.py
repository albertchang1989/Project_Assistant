from work_assistant.config import Settings


def test_settings_defaults_to_fake_provider(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)
    monkeypatch.delenv("QWEN_MODEL", raising=False)

    settings = Settings(_env_file=None)

    assert settings.llm_provider == "fake"
    assert settings.qwen_model == "qwen-plus"


def test_settings_accepts_database_url_override():
    settings = Settings(database_url="sqlite:///./custom.db")

    assert settings.database_url == "sqlite:///./custom.db"


def test_settings_ignores_unrelated_environment_keys(monkeypatch):
    monkeypatch.delenv("LLM_PROVIDER", raising=False)

    settings = Settings(_env_file=None, unrelated_secret="value")

    assert settings.llm_provider == "fake"
