from work_assistant.llm.base import LLMAnalysis, LLMProvider
from work_assistant.schemas import WorkItemCreate


class FakeLLMProvider(LLMProvider):
    def analyze_message(self, message: str) -> LLMAnalysis:
        normalized_message = message.upper()
        if "CTR" in normalized_message or "模型" in message:
            work_item = WorkItemCreate(
                title="排查排序模型线上 CTR 下降",
                original_input=message,
                item_type="线上异常",
                priority="高",
                technical_context={"metric": "CTR", "module": "排序模型"},
            )
            return LLMAnalysis(
                intent="new_item",
                work_item=work_item,
                reply="已记录为高优先级线上异常，建议先分渠道查看 CTR 变化，再排查排序模型最近发布和特征输入。",
                confidence=0.9,
            )

        work_item = WorkItemCreate(title=message[:80], original_input=message)
        return LLMAnalysis(
            intent="new_item",
            work_item=work_item,
            reply="我已记录，会继续帮你补齐目标和下一步。",
        )
