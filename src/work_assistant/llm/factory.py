from work_assistant.config import Settings
from work_assistant.llm.base import LLMProvider
from work_assistant.llm.fake import FakeLLMProvider
from work_assistant.llm.qwen import QwenProvider


def build_llm_provider(settings: Settings) -> LLMProvider:
    provider_name = settings.llm_provider.strip().lower()

    if provider_name == "fake":
        return FakeLLMProvider()

    if provider_name == "qwen":
        if not settings.qwen_api_key:
            raise ValueError("qwen_api_key is required when llm_provider is qwen")
        return QwenProvider(
            api_key=settings.qwen_api_key,
            base_url=settings.qwen_base_url,
            model=settings.qwen_model,
        )

    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
