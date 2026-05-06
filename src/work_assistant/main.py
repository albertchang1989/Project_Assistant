from fastapi import FastAPI

from work_assistant.config import get_settings
from work_assistant.db import engine
from work_assistant.dingtalk.router import router as dingtalk_router
from work_assistant.llm.factory import build_llm_provider
from work_assistant.models import Base
from work_assistant.scheduler import build_scheduler


def create_app(init_db: bool = True) -> FastAPI:
    app = FastAPI(title="DingTalk AI Work Assistant")
    settings = get_settings()
    if settings.app_env == "production" and not settings.dingtalk_app_secret:
        raise ValueError("DINGTALK_APP_SECRET is required in production")

    app.state.settings = settings
    app.state.llm_provider = build_llm_provider(settings)

    if init_db:
        Base.metadata.create_all(engine)
    app.include_router(dingtalk_router)

    if settings.app_env == "production":
        app.state.scheduler = build_scheduler(settings.dingtalk_outgoing_webhook)
        app.state.scheduler.start()

        def shutdown_scheduler() -> None:
            if app.state.scheduler.running:
                app.state.scheduler.shutdown()

        app.router.on_shutdown.append(shutdown_scheduler)

    @app.get("/health")
    def health_check() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
