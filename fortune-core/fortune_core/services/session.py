from .fortune_session import FortuneSessionService
__all__ = ["FortuneSessionService"]

server/fortune_session.py

from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from fortune_core.services.fortune_session import FortuneSessionService
router = APIRouter(
    prefix="/fortune/session",
    tags=["fortune-session"],
)
_service = FortuneSessionService()
class SessionCreateRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    system: str = "unified"
    theme: str = "general"
class SessionResponse(BaseModel):
    session_id: str
    question: str
    system: str
    theme: str
    history_ids: list[str]
    favorite_ids: list[str]
@router.post("", response_model=SessionResponse)
def create_session(
    request: SessionCreateRequest,
) -> SessionResponse:
    session = _service.create(
        question=request.question,
        system=request.system,
        theme=request.theme,
    )
    return SessionResponse(**session.to_dict())
@router.get(
    "/{session_id}",
    response_model=SessionResponse,
)
def get_session(session_id: str) -> SessionResponse:
    session = _service.get(session_id)
    if session is None:
        raise HTTPException(
            status_code=404,
            detail="session not found",
        )
    return SessionResponse(**session.to_dict())
@router.delete("/{session_id}")
def delete_session(session_id: str) -> dict[str, bool]:
    if not _service.delete(session_id):
        raise HTTPException(
            status_code=404,
            detail="session not found",
        )
    return {"deleted": True}
