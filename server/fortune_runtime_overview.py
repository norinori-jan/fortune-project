from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_overview import (
    FortuneRuntimeOverviewService,
)


router = APIRouter(
    prefix="/fortune/overview",
    tags=["fortune-overview"],
)

_service = FortuneRuntimeOverviewService()


@router.get("")
def runtime_overview() -> dict:
    return _service.get().to_dict()