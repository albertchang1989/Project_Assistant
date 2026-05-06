import httpx

from work_assistant.llm.qwen import QwenProvider


def test_qwen_provider_parses_structured_response():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.headers["Authorization"] == "Bearer test-key"
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {
                            "content": (
                                '{"intent":"new_item","reply":"已记录，并建议先确认分渠道指标。",'
                                '"work_item":{"title":"排查 CTR 下降","original_input":"CTR 掉了",'
                                '"item_type":"线上异常","goal":"定位原因","status":"待推进",'
                                '"priority":"高","risk_level":"高","collaborators":[],"next_action":"确认分渠道指标",'
                                '"technical_context":{"metric":"CTR"},"conversation_summary":"线上效果异常"}}'
                            )
                        }
                    }
                ]
            },
        )

    client = httpx.Client(transport=httpx.MockTransport(handler))
    provider = QwenProvider(api_key="test-key", base_url="https://example.test/v1", model="qwen-plus", client=client)

    result = provider.analyze_message("CTR 掉了")

    assert result.intent == "new_item"
    assert result.work_item.title == "排查 CTR 下降"
    assert result.work_item.technical_context["metric"] == "CTR"
