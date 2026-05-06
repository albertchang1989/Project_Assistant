from work_assistant.db import build_engine, build_session_factory
from work_assistant.llm.fake import FakeLLMProvider
from work_assistant.models import Base
from work_assistant.repositories import WorkItemRepository
from work_assistant.services.assistant_service import AssistantService


def test_assistant_service_persists_new_work_item():
    engine = build_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session_factory = build_session_factory(engine)

    with session_factory() as session:
        repo = WorkItemRepository(session)
        service = AssistantService(repo=repo, llm=FakeLLMProvider())

        result = service.handle_user_message("今天排序模型线上 CTR 掉了，需要看一下")
        session.commit()

        open_items = repo.list_open_items()

    assert result.created_item_id == open_items[0].id
    assert "高优先级线上异常" in result.reply
