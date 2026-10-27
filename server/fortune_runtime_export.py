from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_export import (
    FortuneRuntimeExportService,
)


router = APIRouter(
    prefix="/fortune/export",
    tags=["fortune-export"],
)

_service = FortuneRuntimeExportService()


@router.get("/{user_key}")
def export_user_runtime(
    user_key: str,
) -> dict:
    return _service.export(user_key).to_dict()