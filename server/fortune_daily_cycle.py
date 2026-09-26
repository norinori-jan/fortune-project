from __future__ import annotations
from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.daily_cycle import DailyCycleService
router = APIRouter(
    prefix="/fortune/daily-cycle",
    tags=["fortune-daily-cycle"],
)
_service = DailyCycleService()
class DailyCycleRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    target_date: date | None = None
class DailyCycleResponse(BaseModel):
    date: str
    items: list[dict]
@router.post("", response_model=DailyCycleResponse)
def create_daily_cycle(
    request: DailyCycleRequest,
) -> DailyCycleResponse:
    result = _service.build(
        question=request.question,
        target_date=request.target_date,
    )
    return DailyCycleResponse(**result.to_dict())