import httpx
import pytest

from work_assistant.dingtalk.client import DingTalkClient
from work_assistant.scheduler import build_scheduler


def test_dingtalk_client_sends_text_message():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["json"] = request.read().decode("utf-8")
        return httpx.Response(200, json={"errcode": 0, "errmsg": "ok"})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    dingtalk = DingTalkClient(webhook="https://example.test/webhook", client=client)

    dingtalk.send_text("今日关注：暂无风险。")

    assert "今日关注" in captured["json"]


def test_dingtalk_client_noops_without_webhook():
    def handler(request: httpx.Request) -> httpx.Response:
        raise AssertionError("empty webhook should not issue a request")

    client = httpx.Client(transport=httpx.MockTransport(handler))
    dingtalk = DingTalkClient(webhook="", client=client)

    dingtalk.send_text("不会发送")


def test_dingtalk_client_raises_for_non_2xx_response():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(500, json={"errcode": 1, "errmsg": "failed"})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    dingtalk = DingTalkClient(webhook="https://example.test/webhook", client=client)

    with pytest.raises(httpx.HTTPStatusError):
        dingtalk.send_text("今日关注：接口异常。")


def test_dingtalk_client_raises_for_nonzero_errcode():
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"errcode": 310000, "errmsg": "keywords not in content"})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    dingtalk = DingTalkClient(webhook="https://example.test/webhook", client=client)

    with pytest.raises(RuntimeError, match="DingTalk webhook failed"):
        dingtalk.send_text("今日关注：接口异常。")


def test_build_scheduler_creates_weekday_shanghai_report_jobs():
    scheduler = build_scheduler("https://example.test/webhook")

    jobs = scheduler.get_jobs()

    assert str(scheduler.timezone) == "Asia/Shanghai"
    assert [job.func.__name__ for job in jobs] == [
        "send_morning_report",
        "send_evening_report",
    ]
    assert [str(job.trigger) for job in jobs] == [
        "cron[day_of_week='mon-fri', hour='9', minute='30']",
        "cron[day_of_week='mon-fri', hour='18', minute='30']",
    ]
    assert [job.args for job in jobs] == [
        ("https://example.test/webhook",),
        ("https://example.test/webhook",),
    ]
