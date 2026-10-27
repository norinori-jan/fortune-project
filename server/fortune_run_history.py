from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Query
from fortune_core.services.fortune_run_history import (
    FortuneRunHistoryService,
)
router = APIRouter(
    prefix="/fortune/runs",
    tags=["fortune-runs"],
)
_service = FortuneRunHistoryService()
@router.get("")
def list_runs(
    limit: int = Query(
        default=20,
        ge=1,
        le=100,
    ),
) -> dict[str, Any]:
    items = _service.list(limit)
    return {
        "items": [
            item.to_dict()
            for item in items
        ],
        "total": len(items),
    }
@router.get("/{execution_id}")
def get_run(
    execution_id: str,
) -> dict[str, Any]:
    item = _service.get(execution_id)
    if item is None:
        return {
            "found": False,
            "execution_id": execution_id,
        }
    return {
        "found": True,
        "item": item.to_dict(),
    }
