from __future__ import annotations
from datetime import date
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_hub import FortuneHubService
router = APIRouter(
    prefix="/fortune/hub",
    tags=["fortune-hub"],
)
_service = FortuneHubService()
class FortuneHubRequest(BaseModel):
    birth_date: str | None = Field(
        default=None,
        description="Birth date in YYYY-MM-DD format.",
    )
    question: str = Field(
        default="",
        max_length=500,
    )
    theme: str = Field(
        default="general",
        max_length=50,
    )
class FortuneHubQuickRequest(BaseModel):
    question: str = Field(
        default="",
        max_length=500,
    )
    theme: str = Field(
        default="general",
        max_length=50,
    )
@router.post("/home")
def fortune_hub_home(
    request: FortuneHubRequest,
) -> dict[str, Any]:
    result = _service.home(
        birth_date=request.birth_date,
        question=request.question,
        theme=request.theme,
    )
    return result.to_dict()
@router.post("/quick")
def fortune_hub_quick(
    request: FortuneHubQuickRequest,
) -> dict[str, Any]:
    return _service.quick(
        question=request.question,
        theme=request.theme,
    )
@router.get("/today")
def fortune_hub_today(
    theme: str = "general",
) -> dict[str, Any]:
    return _service.quick(
        question="",
        theme=theme,
        today=date.today(),
    )
