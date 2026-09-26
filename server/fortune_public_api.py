from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_gateway import FortuneRuntimeGateway
from fortune_core.services.runtime_public import FortuneRuntimePublicService
router = APIRouter(
    prefix="/fortune/public",
    tags=["fortune-public"],
)
_gateway = FortuneRuntimeGateway()
_public = FortuneRuntimePublicService()
class PublicFortuneRequest(BaseModel):
    user_key: str = "anonymous"
    question: str = ""
    theme: str = "general"
    operation: str = "quick"
@router.post("/fortune")
def public_fortune(
    payload: PublicFortuneRequest,
) -> dict[str, Any]:
    request = HubRuntimeRequest(
        user_key=payload.user_key,
        question=payload.question,
        theme=payload.theme,
        operation=payload.operation,
    )
    result = _gateway.execute(request)
    return _public.response(result)
