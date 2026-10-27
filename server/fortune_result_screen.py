from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from fortune_core.services.screen_result import (
    FortuneResultScreenService,
)


router = APIRouter(
    prefix="/fortune/result-screen",
    tags=["fortune-result-screen"],
)

_service = FortuneResultScreenService()


@router.post("")
def result_screen(
    system: str,
    theme: str,
    result: dict[str, Any],
) -> dict:
    return _service.build(
        system=system,
        theme=theme,
        result=result,
    ).to_dict()