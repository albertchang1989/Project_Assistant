from datetime import UTC, datetime, timedelta

from work_assistant.db import build_engine, build_session_factory
from work_assistant.models import Base
from work_assistant.repositories import WorkItemRepository
from work_assistant.schemas import WorkItemCreate


def make_repo():
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)
    session = session_factory()
    return WorkItemRepository(session), session


def test_create_and_get_open_items():
    repo, session = make_repo()
    try:
        item = repo.create(
            WorkItemCreate(
                title="排查排序模型 CTR 下降",
                original_input="今天排序模型线上 CTR 掉了，需要看一下",
                item_type="线上异常",
                goal="定位 CTR 下降原因",
                due_at=datetime.now(UTC) + timedelta(days=1),
                status="待推进",
                priority="高",
                risk_level="高",
                collaborators=["数据同学"],
                next_action="拉取分渠道指标和最近变更列表",
                technical_context={"metric": "CTR", "module": "排序模型"},
                conversation_summary="用户记录线上 CTR 下降问题",
            )
        )
        session.commit()

        open_items = repo.list_open_items()

        assert len(open_items) == 1
        assert open_items[0].id == item.id
        assert open_items[0].technical_context["metric"] == "CTR"
    finally:
        session.close()
