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

fortune-core/fortune_core/models/favorite.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FavoriteFortune:
    favorite_id: str
    name: str
    question: str
    system: str
    created_at: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.favorite_id,
            "name": self.name,
            "question": self.question,
            "system": self.system,
            "created_at": self.created_at,
        }