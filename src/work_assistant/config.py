from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_env: str = "local"
    database_url: str = "sqlite:///./work_assistant.db"
    llm_provider: str = "fake"
    qwen_api_key: str = ""
    qwen_base_url: str = "https://dashscope.aliyuncs.com/compatible-mode/v1"
    qwen_model: str = "qwen-plus"
    dingtalk_app_secret: str = ""
    dingtalk_outgoing_webhook: str = ""
    morning_report_cron: str = "0 30 9 * * MON-FRI"
    evening_report_cron: str = "0 30 18 * * MON-FRI"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


def get_settings() -> Settings:
    return Settings()
