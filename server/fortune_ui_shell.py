from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.ui_shell import (
    FortuneUiShellService,
)


router = APIRouter(
    prefix="/fortune/shell",
    tags=["fortune-ui-shell"],
)

_service = FortuneUiShellService()


@router.get("/{user_key}")
def ui_shell(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.build(
        user_key=user_key,
        theme=theme,
    )