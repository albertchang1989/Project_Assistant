from work_assistant.llm.fake import FakeLLMProvider


def test_fake_provider_detects_algorithm_incident():
    provider = FakeLLMProvider()

    result = provider.analyze_message("今天排序模型线上 CTR 掉了，需要看一下")

    assert result.intent == "new_item"
    assert result.work_item.title == "排查排序模型线上 CTR 下降"
    assert result.work_item.item_type == "线上异常"
    assert result.work_item.technical_context["metric"] == "CTR"
    assert "分渠道" in result.reply


def test_fake_provider_detects_lowercase_ctr():
    provider = FakeLLMProvider()

    result = provider.analyze_message("今天排序线上 ctr 掉了，需要看一下")

    assert result.work_item.item_type == "线上异常"
    assert result.work_item.technical_context["metric"] == "CTR"
