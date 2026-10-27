from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_config import (
    FortuneRuntimeConfigService,
)
from fortune_core.services.runtime_history import (
    FortuneRuntimeHistoryService,
)
from fortune_core.services.runtime_orchestrator import (
    FortuneRuntimeOrchestrator,
)
from fortune_core.services.theme_router import (
    FortuneThemeRouterService,
)
router = APIRouter(
    prefix="/fortune/orchestrator",
    tags=["fortune-orchestrator"],
)
_orchestrator = FortuneRuntimeOrchestrator()
_config = FortuneRuntimeConfigService()
_history = _orchestrator.history
_theme_router = FortuneThemeRouterService()
class OrchestratorRequest(BaseModel):
    user_key: str = "anonymous"
    question: str = ""
    theme: str = "general"
    operation: str = "home"
    use_cache: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)
@router.post("/execute")
def orchestrator_execute(
    payload: OrchestratorRequest,
) -> dict[str, Any]:
    request = HubRuntimeRequest(
        user_key=payload.user_key,
        question=payload.question,
        theme=payload.theme,
        operation=payload.operation,
        use_cache=payload.use_cache,
        metadata=payload.metadata,
    )
    return _orchestrator.execute(request)
@router.get("/config")
def orchestrator_config() -> dict[str, Any]:
    return _config.as_dict()
@router.get("/history")
def orchestrator_history(
    user_key: str | None = None,
    operation: str | None = None,
) -> list[dict[str, Any]]:
    return [
        item.to_dict()
        for item in _history.list(
            user_key=user_key,
            operation=operation,
        )
    ]
@router.get("/history/latest")
def orchestrator_latest(
    user_key: str,
) -> dict[str, Any]:
    item = _history.latest(user_key)
    if item is None:
        return {
            "found": False,
            "user_key": user_key,
        }
    return {
        "found": True,
        "record": item.to_dict(),
    }
@router.get("/themes")
def orchestrator_themes() -> list[dict[str, Any]]:
    return [
        item.to_dict()
        for item in _theme_router.list()
    ]
