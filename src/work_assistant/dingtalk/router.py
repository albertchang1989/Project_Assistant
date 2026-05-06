from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from work_assistant.db import get_session
from work_assistant.dingtalk.security import verify_dingtalk_signature
from work_assistant.repositories import WorkItemRepository
from work_assistant.services.assistant_service import AssistantService

router = APIRouter(prefix="/dingtalk", tags=["dingtalk"])


@router.post("/callback")
def dingtalk_callback(
    request: Request,
    payload: dict[str, Any],
    timestamp: str = Query(default=""),
    sign: str = Query(default=""),
    session: Session = Depends(get_session),
) -> dict[str, dict[str, str] | str]:
    settings = request.app.state.settings
    if not verify_dingtalk_signature(timestamp, sign, settings.dingtalk_app_secret):
        raise HTTPException(status_code=401, detail="Invalid DingTalk signature")

    message = payload.get("text", {}).get("content", "").strip()
    if not message:
        return {"msgtype": "text", "text": {"content": "我没有收到可记录的文字内容。"}}

    service = AssistantService(repo=WorkItemRepository(session), llm=request.app.state.llm_provider)
    result = service.handle_user_message(message)
    session.commit()
    return {"msgtype": "text", "text": {"content": result.reply}}
