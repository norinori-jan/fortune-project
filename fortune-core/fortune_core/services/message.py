from __future__ import annotations
from .fortune_message import FortuneMessageService
__all__ = ["FortuneMessageService"]

# [貼り付けメモ] server/fortune_message.py

from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_message import FortuneMessageService
router = APIRouter(
    prefix="/fortune/message",
    tags=["fortune-message"],
)
_service = FortuneMessageService()
class MessageRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    target_date: date | None = None
class MessageResponse(BaseModel):
    id: str
    category: str
    title: str
    message: str
    keyword: str
@router.post("", response_model=MessageResponse)
def create_message(
    request: MessageRequest,
) -> MessageResponse:
    result = _service.build(
        question=request.question,
        target_date=request.target_date,
    )
    return MessageResponse(**result.to_dict())
