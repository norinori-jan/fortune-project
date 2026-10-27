from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_gateway import FortuneRuntimeGateway
from fortune_core.services.runtime_subscriptions import (
    FortuneRuntimeSubscriptionService,
)
router = APIRouter(
    prefix="/fortune/gateway",
    tags=["fortune-gateway"],
)
_gateway = FortuneRuntimeGateway()
_subscriptions = FortuneRuntimeSubscriptionService()
class GatewayRequest(BaseModel):
    user_key: str = "anonymous"
    question: str = ""
    theme: str = "general"
    operation: str = "home"
    use_cache: bool = True
    metadata: dict[str, Any] = Field(default_factory=dict)
class SubscriptionRequest(BaseModel):
    subscription_id: str
    event_type: str
def _request(payload: GatewayRequest) -> HubRuntimeRequest:
    return HubRuntimeRequest(
        user_key=payload.user_key,
        question=payload.question,
        theme=payload.theme,
        operation=payload.operation,
        use_cache=payload.use_cache,
        metadata=payload.metadata,
    )
@router.post("/execute")
def gateway_execute(
    payload: GatewayRequest,
) -> dict[str, Any]:
    return _gateway.execute(_request(payload))
@router.post("/submit")
def gateway_submit(
    payload: GatewayRequest,
) -> dict[str, Any]:
    return _gateway.submit(_request(payload))
@router.get("/jobs")
def gateway_jobs(
    user_key: str | None = None,
) -> list[dict[str, Any]]:
    return [
        item.to_dict()
        for item in _gateway.jobs.list(user_key=user_key)
    ]
@router.get("/jobs/{job_id}")
def gateway_job(job_id: str) -> dict[str, Any]:
    job = _gateway.jobs.get(job_id)
    if job is None:
        return {
            "found": False,
            "job_id": job_id,
        }
    return {
        "found": True,
        "job": job.to_dict(),
    }
@router.get("/audit")
def gateway_audit(
    user_key: str | None = None,
    request_id: str | None = None,
) -> list[dict[str, Any]]:
    return [
        item.to_dict()
        for item in _gateway.audit.list(
            user_key=user_key,
            request_id=request_id,
        )
    ]
@router.post("/subscriptions")
def gateway_subscribe(
    payload: SubscriptionRequest,
) -> dict[str, Any]:
    item = _subscriptions.subscribe(
        subscription_id=payload.subscription_id,
        event_type=payload.event_type,
    )
    return item.to_dict()
@router.delete("/subscriptions/{subscription_id}")
def gateway_unsubscribe(
    subscription_id: str,
) -> dict[str, Any]:
    return {
        "subscription_id": subscription_id,
        "removed": _subscriptions.unsubscribe(subscription_id),
    }
@router.get("/subscriptions")
def gateway_subscriptions() -> list[dict[str, Any]]:
    return [
        item.to_dict()
        for item in _subscriptions.list()
    ]