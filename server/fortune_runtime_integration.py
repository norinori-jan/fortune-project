from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_integration import (
    FortuneRuntimeIntegrationService,
)
router = APIRouter(
    prefix="/fortune/integration",
    tags=["fortune-integration"],
)
_service = FortuneRuntimeIntegrationService()
class IntegrationRequest(BaseModel):
    user_key: str = "anonymous"
    session_id: str | None = None
    question: str = ""
    theme: str = "general"
    operation: str = "home"
@router.post("/execute")
def integration_execute(
    payload: IntegrationRequest,
) -> dict[str, Any]:
    return _service.execute(
        HubRuntimeRequest(
            user_key=payload.user_key,
            question=payload.question,
            theme=payload.theme,
            operation=payload.operation,
        ),
        session_id=payload.session_id,
    )
@router.get("/home/{user_key}")
def integration_home(
    user_key: str,
    theme: str = "general",
    session_id: str | None = None,
) -> dict[str, Any]:
    return _service.home(
        user_key=user_key,
        theme=theme,
        session_id=session_id,
    )
@router.get("/today/{user_key}")
def integration_today(
    user_key: str,
    theme: str = "general",
    session_id: str | None = None,
) -> dict[str, Any]:
    return _service.today(
        user_key=user_key,
        theme=theme,
        session_id=session_id,
    )
@router.post("/quick/{user_key}")
def integration_quick(
    user_key: str,
    question: str,
    theme: str = "general",
    session_id: str | None = None,
) -> dict[str, Any]:
    return _service.quick(
        user_key=user_key,
        question=question,
        theme=theme,
        session_id=session_id,
    )
@router.get("/catalog")
def integration_catalog() -> dict[str, Any]:
    return _service.catalog()
