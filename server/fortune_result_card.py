from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from fortune_core.services.result_card import (
    FortuneResultCardService,
)


router = APIRouter(
    prefix="/fortune/result-card",
    tags=["fortune-result-card"],
)

_service = FortuneResultCardService()


@router.post("")
def result_card(
    system: str,
    theme: str,
    result: dict[str, Any],
) -> dict:
    return _service.build(
        system=system,
        theme=theme,
        result=result,
    ).to_dict()