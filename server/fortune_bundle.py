from __future__ import annotations
from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_bundle import FortuneBundleService
router = APIRouter(
    prefix="/fortune/bundle",
    tags=["fortune-bundle"],
)
_service = FortuneBundleService()
class BundleRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    target_date: date | None = None
class BundleResponse(BaseModel):
    question: str
    date: str
    summary: dict
    cards: list[dict]
@router.post("", response_model=BundleResponse)
def create_bundle(
    request: BundleRequest,
) -> BundleResponse:
    result = _service.build(
        question=request.question,
        target_date=request.target_date,
    )
    return BundleResponse(**result.to_dict())
