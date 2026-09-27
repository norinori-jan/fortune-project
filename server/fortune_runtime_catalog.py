from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from fortune_core.services.runtime_catalog import (
    FortuneRuntimeCatalogService,
)
router = APIRouter(
    prefix="/fortune/runtime-catalog",
    tags=["fortune-runtime-catalog"],
)
_catalog = FortuneRuntimeCatalogService()
@router.get("")
def runtime_catalog() -> dict[str, Any]:
    return _catalog.catalog()