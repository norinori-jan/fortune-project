from __future__ import annotations
from datetime import date
from typing import Any
from fastapi import APIRouter, Query
from fortune_core.services.hub_action import FortuneHubActionService
router = APIRouter(
    prefix="/fortune/actions",
    tags=["fortune-actions"],
)
_service = FortuneHubActionService()
@router.get("")
def actions(
    theme: str = Query(default="general"),
    limit: int = Query(default=3, ge=1, le=10),
) -> dict[str, Any]:
    result = _service.generate(
        theme=theme,
        target_date=date.today(),
        limit=limit,
    )
    return {
        "theme": theme,
        "date": date.today().isoformat(),
        "items": [
            item.to_dict()
            for item in result
        ],
    }