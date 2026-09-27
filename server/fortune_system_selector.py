from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.system_selector import (
    FortuneSystemSelectorService,
)


router = APIRouter(
    prefix="/fortune/systems",
    tags=["fortune-systems"],
)

_service = FortuneSystemSelectorService()


@router.get("")
def systems(
    theme: str = "general",
) -> list[dict]:
    return [
        item.to_dict()
        for item in _service.list(theme)
    ]


@router.get("/{system}")
def system(
    system: str,
) -> dict:
    item = _service.get(system)

    if item is None:
        return {
            "found": False,
            "system": system,
        }

    return {
        "found": True,
        "system": item.to_dict(),
    }