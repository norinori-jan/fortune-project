from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_daily import (
    FortuneRuntimeDailyService,
)


router = APIRouter(
    prefix="/fortune/runtime-daily",
    tags=["fortune-runtime-daily"],
)

_service = FortuneRuntimeDailyService()


@router.get("/{user_key}")
def runtime_daily(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.get(
        user_key=user_key,
        theme=theme,
    ).to_dict()