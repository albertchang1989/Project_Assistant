from work_assistant.config import Settings
from work_assistant.llm.factory import build_llm_provider
from work_assistant.llm.fake import FakeLLMProvider
from work_assistant.llm.qwen import QwenProvider


def test_factory_builds_fake_provider():
    provider = build_llm_provider(Settings(llm_provider="fake"))

    assert isinstance(provider, FakeLLMProvider)


def test_factory_builds_qwen_provider():
    provider = build_llm_provider(Settings(llm_provider="qwen", qwen_api_key="key"))

    assert isinstance(provider, QwenProvider)


def test_factory_rejects_qwen_without_api_key():
    try:
        build_llm_provider(Settings(llm_provider="qwen"))
    except ValueError as exc:
        assert "qwen_api_key" in str(exc)
    else:
        raise AssertionError("Expected ValueError")


def test_factory_rejects_unknown_provider():
    try:
        build_llm_provider(Settings(llm_provider="unknown"))
    except ValueError as exc:
        assert "unknown llm provider" in str(exc).lower()
    else:
        raise AssertionError("Expected ValueError")
