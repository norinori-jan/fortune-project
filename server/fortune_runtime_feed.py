from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_feed import (
    FortuneRuntimeFeedService,
)


router = APIRouter(
    prefix="/fortune/runtime-feed",
    tags=["fortune-runtime-feed"],
)

_service = FortuneRuntimeFeedService()


@router.get("/{user_key}")
def runtime_feed(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.build(
        user_key=user_key,
        theme=theme,
    )