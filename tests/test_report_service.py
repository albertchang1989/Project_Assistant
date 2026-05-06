from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

from work_assistant.db import build_engine, build_session_factory
from work_assistant.models import Base
from work_assistant.repositories import WorkItemRepository
from work_assistant.schemas import WorkItemCreate
from work_assistant.services.report_service import ReportService


def test_morning_report_prioritizes_high_risk_items():
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    with session_factory() as session:
        repo = WorkItemRepository(session)
        repo.create(
            WorkItemCreate(
                title="整理本周实验记录",
                original_input="整理本周实验记录",
                item_type="实验",
                due_at=datetime.now(UTC),
                risk_level="低",
                priority="低",
                status="待推进",
                next_action="汇总实验表",
            )
        )
        repo.create(
            WorkItemCreate(
                title="排查排序模型 CTR 下降",
                original_input="今天排序模型线上 CTR 掉了",
                item_type="线上异常",
                due_at=datetime.now(UTC) + timedelta(days=1),
                risk_level="高",
                priority="高",
                status="待推进",
                next_action="拉取分渠道指标",
            )
        )
        session.commit()

        report = ReportService(repo).build_morning_report()

    assert "今日关注" in report
    assert "排查排序模型 CTR 下降" in report
    assert "拉取分渠道指标" in report
    assert report.index("排查排序模型 CTR 下降") < report.index("整理本周实验记录")


def test_morning_sort_key_handles_mixed_datetime_awareness():
    aware_item = SimpleNamespace(
        risk_level="高",
        priority="高",
        due_at=datetime(2026, 5, 5, 9, 0, tzinfo=UTC),
    )
    naive_item = SimpleNamespace(
        risk_level="高",
        priority="高",
        due_at=datetime(2026, 5, 5, 10, 0),
    )

    sorted_items = sorted([naive_item, aware_item], key=ReportService._morning_sort_key)

    assert sorted_items == [aware_item, naive_item]
