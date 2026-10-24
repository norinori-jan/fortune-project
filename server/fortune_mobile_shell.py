from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.mobile_shell import (
    FortuneMobileShellService,
)


router = APIRouter(
    prefix="/fortune/mobile",
    tags=["fortune-mobile"],
)

_service = FortuneMobileShellService()


@router.get("/{user_key}")
def mobile_shell(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.build(
        user_key=user_key,
        theme=theme,
    )