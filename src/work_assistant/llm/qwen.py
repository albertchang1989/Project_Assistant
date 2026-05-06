import json

import httpx

from work_assistant.llm.base import LLMAnalysis, LLMProvider


SYSTEM_PROMPT = """你是一个钉钉里的个人工作助手，服务对象是算法研发工程师。
你要把用户的模糊工作消息转成结构化事项，并在必要时给出 1-2 个关键追问或技术提醒。
只输出 JSON，字段包括 intent、reply、work_item。work_item 字段必须能映射到 WorkItemCreate。
"""


class QwenProvider(LLMProvider):
    def __init__(self, api_key: str, base_url: str, model: str, client: httpx.Client | None = None) -> None:
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.client = client or httpx.Client(timeout=30)

    def analyze_message(self, message: str) -> LLMAnalysis:
        response = self.client.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={
                "model": self.model,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message},
                ],
                "temperature": 0.2,
                "response_format": {"type": "json_object"},
            },
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return LLMAnalysis.model_validate(json.loads(content))
