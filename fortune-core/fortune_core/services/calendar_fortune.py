from __future__ import annotations
from .fortune_calendar_fortune import FortuneCalendarFortuneService
__all__ = ["FortuneCalendarFortuneService"]

# [貼り付けメモ] server/fortune_calendar_fortune.py

from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_calendar_fortune import (
    FortuneCalendarFortuneService,
)
router = APIRouter(
    prefix="/fortune/calendar",
    tags=["fortune-calendar"],
)
_service = FortuneCalendarFortuneService()
class CalendarRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    start_date: date | None = None
    days: int = Field(default=30, ge=1, le=366)
class CalendarResponse(BaseModel):
    items: list[dict]
@router.post("", response_model=CalendarResponse)
def create_calendar(
    request: CalendarRequest,
) -> CalendarResponse:
    result = _service.build(
        question=request.question,
        start_date=request.start_date,
        days=request.days,
    )
    return CalendarResponse(
        items=[item.to_dict() for item in result]
    )
