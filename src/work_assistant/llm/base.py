from typing import Protocol

from pydantic import BaseModel

from work_assistant.schemas import WorkItemCreate


class LLMAnalysis(BaseModel):
    intent: str
    work_item: WorkItemCreate | None = None
    reply: str
    confidence: float = 0.8


class LLMProvider(Protocol):
    def analyze_message(self, message: str) -> LLMAnalysis:
        ...
