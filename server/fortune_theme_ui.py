from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.theme_ui import (
    FortuneThemeUiService,
)


router = APIRouter(
    prefix="/fortune/theme-ui",
    tags=["fortune-theme-ui"],
)

_service = FortuneThemeUiService()


@router.get("/{theme}")
def theme_ui(
    theme: str,
) -> dict:
    return _service.build(theme)