from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_ui_payload import (
    FortuneRuntimeUiPayloadService,
)


router = APIRouter(
    prefix="/fortune/ui",
    tags=["fortune-ui"],
)

_service = FortuneRuntimeUiPayloadService()


@router.get("/{user_key}")
def runtime_ui(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.build(
        user_key=user_key,
        theme=theme,
    ).to_dict()