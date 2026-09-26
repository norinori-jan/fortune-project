from .fortune_share import FortuneShareService
__all__ = ["FortuneShareService"]

server/fortune_share.py

from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_share import FortuneShareService
router = APIRouter(
    prefix="/fortune/share",
    tags=["fortune-share"],
)
_service = FortuneShareService()
class ShareRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    message: str = Field(..., min_length=1, max_length=2000)
    advice: str = Field(..., min_length=1, max_length=2000)
    system: str = "unified"
    theme: str = "general"
    date_key: str
class ShareResponse(BaseModel):
    id: str
    title: str
    message: str
    advice: str
    system: str
    theme: str
    date: str
    encoded: str
@router.post("", response_model=ShareResponse)
def create_share(
    request: ShareRequest,
) -> ShareResponse:
    result = _service.create(
        title=request.title,
        message=request.message,
        advice=request.advice,
        system=request.system,
        theme=request.theme,
        date_key=request.date_key,
    )
    return ShareResponse(
        **result.to_dict(),
        encoded=_service.encode(result),
    )
