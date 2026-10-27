from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.hub_runtime import FortuneHubRuntimeService
from fortune_core.services.hub_status import FortuneHubStatusService
router = APIRouter(
    prefix="/fortune/runtime",
    tags=["fortune-runtime"],
)
_runtime = FortuneHubRuntimeService()
_status = FortuneHubStatusService(
    cache=_runtime.cache,
    events=_runtime.events,
)
class RuntimeRequest(BaseModel):
    user_key: str = Field(default="anonymous", min_length=1)
    question: str = ""
    theme: str = "general"
    operation: str = "home"
    use_cache: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)
@router.post("")
def run_runtime(request: RuntimeRequest) -> dict[str, Any]:
    runtime_request = HubRuntimeRequest(
        user_key=request.user_key,
        question=request.question,
        theme=request.theme,
        operation=request.operation,
        use_cache=request.use_cache,
        metadata=request.metadata,
    )
    return _runtime.execute(runtime_request).to_dict()
@router.get("/status")
def runtime_status() -> dict[str, Any]:
    return _status.status().to_dict()
@router.get("/events")
def runtime_events(
    user_key: str | None = None,
    event_type: str | None = None,
) -> list[dict[str, Any]]:
    return [
        event.to_dict()
        for event in _runtime.events.list(
            user_key=user_key,
            event_type=event_type,
        )
    ]
