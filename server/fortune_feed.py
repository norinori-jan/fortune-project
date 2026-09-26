from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Query
from fortune_core.services.fortune_feed import FortuneFeedService
router = APIRouter(
    prefix="/fortune/feed",
    tags=["fortune-feed"],
)
_service = FortuneFeedService()
@router.get("")
def feed(
    theme: str = Query(default="general"),
    question: str = Query(default=""),
    limit: int = Query(default=10, ge=1, le=30),
) -> dict[str, Any]:
    result = _service.build(
        theme=theme,
        question=question,
        limit=limit,
    )
    return result.to_dict()