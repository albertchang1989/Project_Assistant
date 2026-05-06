from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class WorkItemCreate(BaseModel):
    title: str
    original_input: str
    item_type: str = "任务"
    goal: str | None = None
    due_at: datetime | None = None
    status: str = "待澄清"
    priority: str = "中"
    risk_level: str = "中"
    collaborators: list[str] = Field(default_factory=list)
    next_action: str | None = None
    technical_context: dict[str, Any] = Field(default_factory=dict)
    conversation_summary: str | None = None


class WorkItemRead(WorkItemCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
