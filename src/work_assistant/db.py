from collections.abc import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from work_assistant.config import get_settings


def build_engine(database_url: str) -> Engine:
    connect_args = {"check_same_thread": False} if database_url.startswith("sqlite") else {}
    return create_engine(database_url, connect_args=connect_args)


def build_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


settings = get_settings()
engine = build_engine(settings.database_url)
SessionLocal = build_session_factory(engine)


def get_session() -> Generator[Session, None, None]:
    with SessionLocal() as session:
        yield session
