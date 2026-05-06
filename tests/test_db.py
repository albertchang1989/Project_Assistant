from sqlalchemy import text

from work_assistant.db import build_engine, build_session_factory


def test_session_factory_executes_sql():
    engine = build_engine("sqlite:///:memory:")
    session_factory = build_session_factory(engine)

    with session_factory() as session:
        result = session.execute(text("select 1")).scalar_one()

    assert result == 1
