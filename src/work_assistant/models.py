from datetime import UTC, datetime
from typing import Any

from sqlalchemy import DateTime, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import JSON


class Base(DeclarativeBase):
    pass


class WorkItem(Base):
    __tablename__ = "work_items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    original_input: Mapped[str] = mapped_column(Text, nullable=False)
    item_type: Mapped[str] = mapped_column(String(50), nullable=False, default="任务")
    goal: Mapped[str | None] = mapped_column(Text)
    due_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="待澄清")
    priority: Mapped[str] = mapped_column(String(20), nullable=False, default="中")
    risk_level: Mapped[str] = mapped_column(String(20), nullable=False, default="中")
    collaborators: Mapped[list[str]] = mapped_column(JSON, nullable=False, default=list)
    next_action: Mapped[str | None] = mapped_column(Text)
    technical_context: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    conversation_summary: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
