from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_user import FortuneRuntimeUserService
router = APIRouter(
    prefix="/fortune/user-runtime",
    tags=["fortune-user-runtime"],
)
_service = FortuneRuntimeUserService()
class UserRuntimeRequest(BaseModel):
    user_key: str = "anonymous"
    session_id: str | None = None
    question: str = ""
    theme: str = "general"
    operation: str = "home"
    use_cache: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)
@router.post("/execute")
def user_runtime_execute(
    payload: UserRuntimeRequest,
) -> dict[str, Any]:
    request = HubRuntimeRequest(
        user_key=payload.user_key,
        question=payload.question,
        theme=payload.theme,
        operation=payload.operation,
        use_cache=payload.use_cache,
        metadata=payload.metadata,
    )
    return _service.execute(
        request,
        session_id=payload.session_id,
    )
@router.get("/{user_key}/profile")
def user_runtime_profile(
    user_key: str,
) -> dict[str, Any]:
    return _service.profile(user_key)
@router.get("/{user_key}/summary")
def user_runtime_summary(
    user_key: str,
) -> dict[str, Any]:
    return _service.summary_for(user_key)
@router.get("/{user_key}/recommendations")
def user_runtime_recommendations(
    user_key: str,
    themes: str | None = None,
) -> list[dict[str, Any]]:
    selected = (
        [item.strip() for item in themes.split(",")]
        if themes
        else None
    )
    return _service.recommendations_for(
        user_key=user_key,
        themes=selected,
    )
