from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from fortune_core.services.favorite_fortune import FavoriteFortuneService
router = APIRouter(
    prefix="/fortune/favorites",
    tags=["fortune-favorites"],
)
_service = FavoriteFortuneService()
class FavoriteCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    question: str = Field(..., min_length=1, max_length=500)
    system: str = Field(default="unified", min_length=1, max_length=50)
class FavoriteResponse(BaseModel):
    id: str
    name: str
    question: str
    system: str
    created_at: str
@router.post("", response_model=FavoriteResponse)
def add_favorite(
    request: FavoriteCreateRequest,
) -> FavoriteResponse:
    item = _service.add(
        name=request.name,
        question=request.question,
        system=request.system,
    )
    return FavoriteResponse(**item.to_dict())
@router.get("", response_model=list[FavoriteResponse])
def list_favorites() -> list[FavoriteResponse]:
    return [
        FavoriteResponse(**item.to_dict())
        for item in _service.list()
    ]
@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: str) -> dict[str, bool]:
    if not _service.remove(favorite_id):
        raise HTTPException(status_code=404, detail="favorite not found")
    return {"deleted": True}