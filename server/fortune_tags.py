from fastapi import APIRouter
from pydantic import BaseModel
from fortune_core.services.fortune_tag_search import (
    FortuneTagService,
)
router = APIRouter(
    prefix="/fortune/tags",
    tags=["fortune-tags"],
)
_service = FortuneTagService()
class TagResponse(BaseModel):
    key: str
    label: str
    category: str
@router.get("", response_model=list[TagResponse])
def list_tags(
    q: str = "",
) -> list[TagResponse]:
    return [
        TagResponse(**item.to_dict())
        for item in _service.find(q)
    ]
