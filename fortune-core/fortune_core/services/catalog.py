from .fortune_catalog import FortuneCatalogService
__all__ = ["FortuneCatalogService"]

# [貼り付けメモ] server/fortune_catalog.py

from fastapi import APIRouter
from pydantic import BaseModel
from fortune_core.services.fortune_catalog import (
    FortuneCatalogService,
)
router = APIRouter(
    prefix="/fortune/catalog",
    tags=["fortune-catalog"],
)
_service = FortuneCatalogService()
class CatalogItemResponse(BaseModel):
    key: str
    name: str
    description: str
    category: str
    available: bool
@router.get(
    "/systems",
    response_model=list[CatalogItemResponse],
)
def list_systems() -> list[CatalogItemResponse]:
    return [
        CatalogItemResponse(**item.to_dict())
        for item in _service.systems()
    ]
@router.get(
    "/themes",
    response_model=list[CatalogItemResponse],
)
def list_themes() -> list[CatalogItemResponse]:
    return [
        CatalogItemResponse(**item.to_dict())
        for item in _service.themes()
    ]
@router.get(
    "",
    response_model=list[CatalogItemResponse],
)
def list_catalog() -> list[CatalogItemResponse]:
    return [
        CatalogItemResponse(**item.to_dict())
        for item in _service.all()
    ]
