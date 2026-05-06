# DingTalk AI Work Assistant

Personal DingTalk-based work assistant MVP for recording work items, asking clarifying questions, and sending morning/evening summaries.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env
uvicorn work_assistant.main:create_app --factory --reload
```

## Test

```bash
pytest -v
```

## Initialize Local Database

```bash
python -m work_assistant.bootstrap
```

## Local Callback Smoke Test

```bash
curl -X POST http://127.0.0.1:8000/dingtalk/callback \
  -H 'Content-Type: application/json' \
  -d '{"text":{"content":"今天排序模型线上 CTR 掉了，需要看一下"}}'
```
