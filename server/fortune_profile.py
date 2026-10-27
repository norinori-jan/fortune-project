from __future__ import annotations
from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_profile import FortuneProfileService
router = APIRouter(
    prefix="/fortune/profile",
    tags=["fortune-profile"],
)
_service = FortuneProfileService()
class ProfileRequest(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=50)
    birth_date: date | None = None
    favorite_system: str = "unified"
    favorite_theme: str = "general"
class ProfileResponse(BaseModel):
    id: str
    nickname: str
    birth_date: str | None
    favorite_system: str
    favorite_theme: str
    keywords: list[str]
@router.post("", response_model=ProfileResponse)
def create_profile(
    request: ProfileRequest,
) -> ProfileResponse:
    result = _service.build(
        nickname=request.nickname,
        birth_date=request.birth_date,
        favorite_system=request.favorite_system,
        favorite_theme=request.favorite_theme,
    )
    return ProfileResponse(**result.to_dict())