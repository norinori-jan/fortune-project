from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_bootstrap import (
    FortuneRuntimeBootstrapService,
)


router = APIRouter(
    prefix="/fortune/bootstrap",
    tags=["fortune-bootstrap"],
)

_service = FortuneRuntimeBootstrapService()


@router.get("/{user_key}")
def runtime_bootstrap(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _service.build(
        user_key=user_key,
        theme=theme,
    ).to_dict()