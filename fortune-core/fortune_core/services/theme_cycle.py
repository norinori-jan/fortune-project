from __future__ import annotations
from .fortune_theme_cycle import FortuneThemeCycleService
__all__ = ["FortuneThemeCycleService"]

# [貼り付けメモ] server/fortune_theme_cycle.py

from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_theme_cycle import (
    FortuneThemeCycleService,
)
router = APIRouter(
    prefix="/fortune/theme-cycle",
    tags=["fortune-theme-cycle"],
)
_service = FortuneThemeCycleService()
class ThemeCycleRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    period: str = Field(default="week", pattern="^(week|year)$")
    target_date: date | None = None
class ThemeCycleResponse(BaseModel):
    period: str
    period_key: str
    items: list[dict]
@router.post("", response_model=ThemeCycleResponse)
def create_theme_cycle(
    request: ThemeCycleRequest,
) -> ThemeCycleResponse:
    result = _service.build(
        question=request.question,
        period=request.period,
        target_date=request.target_date,
    )
    return ThemeCycleResponse(**result.to_dict())
