from sqlalchemy import select
from sqlalchemy.orm import Session

from work_assistant.models import WorkItem
from work_assistant.schemas import WorkItemCreate


class WorkItemRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def create(self, data: WorkItemCreate) -> WorkItem:
        item = WorkItem(**data.model_dump())
        self.session.add(item)
        self.session.flush()
        return item

    def list_open_items(self) -> list[WorkItem]:
        statement = (
            select(WorkItem)
            .where(WorkItem.status.not_in(["已完成", "已搁置"]))
            .order_by(WorkItem.updated_at.desc())
        )
        return list(self.session.scalars(statement).all())
