from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from fortune_core.services.hub_navigation import (
    FortuneHubNavigationService,
)
router = APIRouter(
    prefix="/fortune/hub",
    tags=["fortune-hub"],
)
_service = FortuneHubNavigationService()
@router.get("/navigation")
def navigation() -> dict[str, Any]:
    return _service.build().to_dict()