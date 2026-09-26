from .guidance_fortune import FortuneGuidanceService
__all__ = ["FortuneGuidanceService"]

server/fortune_guidance.py

from __future__ import annotations
from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.guidance_fortune import FortuneGuidanceService
router = APIRouter(
    prefix="/fortune/guidance",
    tags=["fortune-guidance"],
)
_service = FortuneGuidanceService()
class GuidanceRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    target_date: date | None = None
class GuidanceResponse(BaseModel):
    actions: list[dict]
    lucky: dict
    timeline: list[str]
    caution: str
@router.post("", response_model=GuidanceResponse)
def create_guidance(
    request: GuidanceRequest,
) -> GuidanceResponse:
    result = _service.build(
        question=request.question,
        target_date=request.target_date,
    )
    return GuidanceResponse(**result.to_dict())