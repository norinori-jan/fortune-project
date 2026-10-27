from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_capabilities import (
    FortuneRuntimeCapabilityService,
)
from fortune_core.services.runtime_facade import FortuneRuntimeFacade
from fortune_core.services.runtime_session import (
    FortuneRuntimeSessionService,
)
router = APIRouter(
    prefix="/fortune/core",
    tags=["fortune-core"],
)
_facade = FortuneRuntimeFacade()
_capabilities = FortuneRuntimeCapabilityService()
_sessions = FortuneRuntimeSessionService()
class CoreFortuneRequest(BaseModel):
    user_key: str = "anonymous"
    session_id: str = "default"
    question: str = ""
    theme: str = "general"
    operation: str = "home"
    use_cache: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)
@router.post("/execute")
def core_execute(
    payload: CoreFortuneRequest,
) -> dict[str, Any]:
    request = HubRuntimeRequest(
        user_key=payload.user_key,
        question=payload.question,
        theme=payload.theme,
        operation=payload.operation,
        use_cache=payload.use_cache,
        metadata=payload.metadata,
    )
    result = _facade.execute(request)
    request_id = result.get("request_id")
    if request_id:
        _sessions.record(
            session_id=payload.session_id,
            request_id=request_id,
            user_key=payload.user_key,
        )
    return result
@router.get("/health")
def core_health() -> dict[str, Any]:
    return _facade.health()
@router.get("/capabilities")
def core_capabilities() -> list[dict[str, Any]]:
    return [
        item.to_dict()
        for item in _capabilities.list()
    ]
@router.get("/sessions/{session_id}")
def core_session(
    session_id: str,
) -> dict[str, Any]:
    session = _sessions.get(session_id)
    if session is None:
        return {
            "found": False,
            "session_id": session_id,
        }
    return {
        "found": True,
        "session": session.to_dict(),
    }
