from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.ui_manifest import (
    FortuneUiManifestService,
)


router = APIRouter(
    prefix="/fortune/ui-manifest",
    tags=["fortune-ui-manifest"],
)

_service = FortuneUiManifestService()


@router.get("")
def ui_manifest() -> dict:
    return _service.build()