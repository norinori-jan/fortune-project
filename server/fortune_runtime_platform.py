from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_platform import (
    FortuneRuntimePlatformService,
)


router = APIRouter(
    prefix="/fortune/platform",
    tags=["fortune-platform"],
)

_service = FortuneRuntimePlatformService()


@router.get("/{user_key}")
def platform_snapshot(
    user_key: str,
) -> dict:
    return _service.snapshot(user_key).to_dict()


@router.get("/features")
def platform_features() -> list[dict]:
    return _service.users.features_snapshot()