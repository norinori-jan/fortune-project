from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.period_views import (
    FortunePeriodViewService,
)


router = APIRouter(
    prefix="/fortune/period-view",
    tags=["fortune-period-view"],
)

_service = FortunePeriodViewService()


@router.get("/{user_key}")
def period_view(
    user_key: str,
    theme: str = "general",
    period: str = "day",
) -> dict:
    return _service.get(
        user_key=user_key,
        theme=theme,
        period=period,
    ).to_dict()