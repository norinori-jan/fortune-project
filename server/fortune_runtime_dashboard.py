from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_dashboard import (
    FortuneRuntimeDashboardService,
)


router = APIRouter(
    prefix="/fortune/runtime-dashboard",
    tags=["fortune-runtime-dashboard"],
)

_service = FortuneRuntimeDashboardService()


@router.get("/{user_key}")
def runtime_dashboard(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.build(
        user_key=user_key,
        theme=theme,
    ).to_dict()