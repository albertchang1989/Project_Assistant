from datetime import UTC, datetime

from work_assistant.models import WorkItem
from work_assistant.repositories import WorkItemRepository


class ReportService:
    def __init__(self, repo: WorkItemRepository) -> None:
        self.repo = repo

    def build_morning_report(self, limit: int = 5) -> str:
        items = self.repo.list_open_items()
        if not items:
            return "今日关注：暂无需要特别关注的事项。"

        sorted_items = sorted(items, key=self._morning_sort_key)
        lines = ["今日关注："]
        for item in sorted_items[:limit]:
            next_action = item.next_action or "暂无下一步行动"
            lines.append(f"- {item.title}｜状态：{item.status}｜下一步：{next_action}")
        return "\n".join(lines)

    def build_evening_report(self) -> str:
        items = self.repo.list_open_items()
        if not items:
            return "今日总结：今天没有记录新的开放事项。"

        unclear_count = sum(
            1 for item in items if item.status == "待澄清" or not item.next_action
        )
        return (
            "今日总结："
            f"当前共有 {len(items)} 个开放事项，"
            f"其中 {unclear_count} 个需要澄清或补充下一步行动。"
        )

    @staticmethod
    def _morning_sort_key(item: WorkItem) -> tuple[int, int, int, datetime]:
        risk_rank = {"高": 0, "中": 1, "低": 2}.get(item.risk_level, 3)
        priority_rank = {"高": 0, "中": 1, "低": 2}.get(item.priority, 3)
        due_rank = 0 if item.due_at is not None else 1
        due_at = ReportService._as_utc_datetime(item.due_at)
        return (risk_rank, priority_rank, due_rank, due_at)

    @staticmethod
    def _as_utc_datetime(value: datetime | None) -> datetime:
        if value is None:
            return datetime.max.replace(tzinfo=UTC)
        if value.tzinfo is None:
            return value.replace(tzinfo=UTC)
        return value.astimezone(UTC)
