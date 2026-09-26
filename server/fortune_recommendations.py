from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Query
from pydantic import BaseModel, Field
from fortune_core.services.recommendation import (
    FortuneRecommendationService,
)
router = APIRouter(
    prefix="/fortune/recommendations",
    tags=["fortune-recommendations"],
)
_service = FortuneRecommendationService()
class RecommendationRequest(BaseModel):
    question: str = Field(default="", max_length=500)
    theme: str = Field(default="general", max_length=50)
    limit: int = Field(default=3, ge=1, le=10)
@router.post("")
def recommend(
    request: RecommendationRequest,
) -> dict[str, Any]:
    items = _service.recommend(
        question=request.question,
        theme=request.theme,
        limit=request.limit,
    )
    return {
        "question": request.question,
        "theme": request.theme,
        "items": [
            item.to_dict()
            for item in items
        ],
    }
@router.get("")
def recommend_get(
    theme: str = Query(default="general"),
    question: str = Query(default=""),
    limit: int = Query(default=3, ge=1, le=10),
) -> dict[str, Any]:
    items = _service.recommend(
        question=question,
        theme=theme,
        limit=limit,
    )
    return {
        "question": question,
        "theme": theme,
        "items": [
            item.to_dict()
            for item in items
        ],
    }
