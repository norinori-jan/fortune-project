from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.hub_widget_feed import (
    FortuneHubWidgetFeedService,
)


router = APIRouter(
    prefix="/fortune/widget-feed",
    tags=["fortune-widget-feed"],
)

_service = FortuneHubWidgetFeedService()


@router.get("/{user_key}")
def widget_feed(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.build(
        user_key=user_key,
        theme=theme,
    )