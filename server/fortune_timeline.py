from __future__ import annotations
from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_timeline import FortuneTimelineService
router = APIRouter(
    prefix="/fortune/timeline",
    tags=["fortune-timeline"],
)
_service = FortuneTimelineService()
class TimelineRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    start_date: date | None = None
    days: int = Field(default=7, ge=1, le=31)
class TimelineResponse(BaseModel):
    items: list[dict]
@router.post("", response_model=TimelineResponse)
def create_timeline(
    request: TimelineRequest,
) -> TimelineResponse:
    result = _service.build(
        question=request.question,
        start_date=request.start_date,
        days=request.days,
    )
    return TimelineResponse(
        items=[item.to_dict() for item in result]
    )