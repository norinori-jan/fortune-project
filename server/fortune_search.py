from __future__ import annotations
from typing import Any
from fastapi import APIRouter, Query
from fortune_core.services.fortune_index import FortuneIndexService
router = APIRouter(
    prefix="/fortune/search",
    tags=["fortune-search"],
)
_service = FortuneIndexService()
@router.get("")
def search(
    q: str = Query(default="", max_length=200),
    theme: str | None = Query(default=None),
    system: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
) -> dict[str, Any]:
    result = _service.search(
        query=q,
        theme=theme,
        system=system,
        limit=limit,
    )
    return result.to_dict()
@router.get("/stats")
def stats() -> dict[str, int]:
    return {
        "indexed_results": _service.size(),
    }