from __future__ import annotations
from .fortune_notification import FortuneNotificationService
__all__ = ["FortuneNotificationService"]

# [貼り付けメモ] server/fortune_notifications.py

from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_notification import (
    FortuneNotificationService,
)
router = APIRouter(
    prefix="/fortune/notifications",
    tags=["fortune-notifications"],
)
_service = FortuneNotificationService()
class NotificationRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    target_date: date | None = None
class NotificationResponse(BaseModel):
    id: str
    title: str
    message: str
    category: str
    timing: str
    enabled: bool
@router.post("", response_model=list[NotificationResponse])
def create_notifications(
    request: NotificationRequest,
) -> list[NotificationResponse]:
    results = _service.build(
        question=request.question,
        target_date=request.target_date,
    )
    return [
        NotificationResponse(**item.to_dict())
        for item in results
    ]
