from sqlalchemy import inspect

from work_assistant.bootstrap import init_database
from work_assistant.db import build_engine


def test_init_database_creates_work_items_table():
    engine = build_engine("sqlite:///:memory:")

    init_database(engine)

    assert "work_items" in inspect(engine).get_table_names()
