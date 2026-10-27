from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_history_items import (
    FortuneRuntimeHistoryItemService,
)


router = APIRouter(
    prefix="/fortune/runtime-history",
    tags=["fortune-runtime-history"],
)

_service = FortuneRuntimeHistoryItemService()


@router.get("/{user_key}")
def runtime_history(
    user_key: str,
    limit: int = 50,
) -> list[dict]:
    return [
        item.to_dict()
        for item in _service.list(
            user_key=user_key,
            limit=limit,
        )
    ]


@router.get("/{user_key}/latest")
def runtime_history_latest(
    user_key: str,
) -> dict | None:
    item = _service.latest(user_key)
    return item.to_dict() if item else None