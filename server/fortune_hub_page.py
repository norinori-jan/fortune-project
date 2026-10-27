from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.hub_page import (
    FortuneHubPageService,
)


router = APIRouter(
    prefix="/fortune/page",
    tags=["fortune-page"],
)

_service = FortuneHubPageService()


@router.get("/home/{user_key}")
def hub_home_page(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.home(
        user_key=user_key,
        theme=theme,
    ).to_dict()