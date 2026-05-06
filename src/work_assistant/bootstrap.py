from sqlalchemy import Engine

from work_assistant.db import engine
from work_assistant.models import Base


def init_database(target_engine: Engine = engine) -> None:
    Base.metadata.create_all(target_engine)


if __name__ == "__main__":
    init_database()
    print("Database initialized.")
