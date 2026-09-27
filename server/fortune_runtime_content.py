from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_content import (
    FortuneRuntimeContentService,
)


router = APIRouter(
    prefix="/fortune/content",
    tags=["fortune-content"],
)

_service = FortuneRuntimeContentService()


@router.get("/{user_key}/daily")
def daily_content(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.daily_content(
        user_key=user_key,
        theme=theme,
    )


@router.get("/{user_key}/weekly")
def weekly_content(
    user_key: str,
    theme: str = "general",
) -> list[dict]:
    return _service.weekly_content(
        user_key=user_key,
        theme=theme,
    )


@router.get("/{user_key}/periods")
def period_content(
    user_key: str,
    theme: str = "general",
) -> list[dict]:
    return _service.period_summary(
        user_key=user_key,
        theme=theme,
    )