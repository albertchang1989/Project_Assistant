from pydantic import BaseModel

from work_assistant.llm.base import LLMProvider
from work_assistant.repositories import WorkItemRepository


class AssistantResult(BaseModel):
    reply: str
    created_item_id: int | None = None


class AssistantService:
    def __init__(self, repo: WorkItemRepository, llm: LLMProvider) -> None:
        self.repo = repo
        self.llm = llm

    def handle_user_message(self, message: str) -> AssistantResult:
        analysis = self.llm.analyze_message(message)
        created_item_id = None

        if analysis.intent == "new_item" and analysis.work_item is not None:
            item = self.repo.create(analysis.work_item)
            created_item_id = item.id

        return AssistantResult(reply=analysis.reply, created_item_id=created_item_id)
