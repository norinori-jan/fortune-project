from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneCompareItem:
    system: str
    title: str
    message: str
    advice: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "system": self.system,
            "title": self.title,
            "message": self.message,
            "advice": self.advice,
        }
@dataclass(frozen=True)
class FortuneComparison:
    question: str
    items: tuple[FortuneCompareItem, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "items": [
                item.to_dict()
                for item in self.items
            ],
        }

fortune-core/fortune_core/services/fortune_compare.py

from __future__ import annotations
from fortune_core.models.fortune_compare import (
    FortuneCompareItem,
    FortuneComparison,
)
from fortune_core.services.complete_fortune import (
    CompleteFortuneService,
)
class FortuneCompareService:
    def __init__(self) -> None:
        self.complete_service = CompleteFortuneService()
    def build(
        self,
        question: str,
    ) -> FortuneComparison:
        result = self.complete_service.divine(question)
        items = (
            FortuneCompareItem(
                system="unified",
                title=result.unified.title,
                message=result.unified.message,
                advice=result.unified.advice,
            ),
            FortuneCompareItem(
                system="tarot",
                title=result.tarot.card.name,
                message=result.tarot.card.message,
                advice=result.tarot.card.advice,
            ),
            FortuneCompareItem(
                system="meihua",
                title=result.meihua.title,
                message=result.meihua.message,
                advice=result.meihua.advice,
            ),
        )
        return FortuneComparison(
            question=question,
            items=items,
        )

fortune-core/fortune_core/services/compare.py

from .fortune_compare import FortuneCompareService
__all__ = ["FortuneCompareService"]

server/fortune_compare.py

from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_compare import FortuneCompareService
router = APIRouter(
    prefix="/fortune/compare",
    tags=["fortune-compare"],
)
_service = FortuneCompareService()
class CompareRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
class CompareResponse(BaseModel):
    question: str
    items: list[dict]
@router.post("", response_model=CompareResponse)
def compare_fortunes(
    request: CompareRequest,
) -> CompareResponse:
    result = _service.build(request.question)
    return CompareResponse(**result.to_dict())