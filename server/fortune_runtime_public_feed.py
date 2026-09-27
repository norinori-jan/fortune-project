from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_public_feed import (
    FortuneRuntimePublicFeedService,
)


router = APIRouter(
    prefix="/fortune/public-feed",
    tags=["fortune-public-feed"],
)

_service = FortuneRuntimePublicFeedService()


@router.get("/{user_key}")
def public_feed(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.home(
        user_key=user_key,
        theme=theme,
    )