from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.app_shell import (
    FortuneAppShellService,
)


router = APIRouter(
    prefix="/fortune/app",
    tags=["fortune-app"],
)

_service = FortuneAppShellService()


@router.get("/{user_key}")
def app_shell(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.build(
        user_key=user_key,
        theme=theme,
    )