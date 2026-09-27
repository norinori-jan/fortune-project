from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_search import (
    FortuneRuntimeSearchService,
)


router = APIRouter(
    prefix="/fortune/runtime-search",
    tags=["fortune-runtime-search"],
)

_service = FortuneRuntimeSearchService()


@router.get("")
def runtime_search(
    q: str,
) -> list[dict]:
    return [
        item.to_dict()
        for item in _service.search(q)
    ]