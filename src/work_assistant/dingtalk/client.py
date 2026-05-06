import httpx


class DingTalkClient:
    def __init__(self, webhook: str, client: httpx.Client | None = None) -> None:
        self.webhook = webhook
        self.client = client or httpx.Client(timeout=10)

    def send_text(self, content: str) -> None:
        if not self.webhook:
            return

        response = self.client.post(
            self.webhook,
            json={"msgtype": "text", "text": {"content": content}},
        )
        response.raise_for_status()
        payload = response.json()
        if payload.get("errcode", 0) != 0:
            errmsg = payload.get("errmsg", "unknown error")
            raise RuntimeError(f"DingTalk webhook failed: {errmsg}")
