from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from fortune_core.services.runtime_event_subscriptions import (
    FortuneRuntimeEventSubscriptionService,
)


router = APIRouter(
    prefix="/fortune/subscriptions",
    tags=["fortune-subscriptions"],
)

_service = FortuneRuntimeEventSubscriptionService()


class SubscriptionRequest(BaseModel):
    user_key: str
    event_types: list[str] = Field(default_factory=list)


@router.post("")
def create_subscription(
    payload: SubscriptionRequest,
) -> dict:
    return _service.create(
        user_key=payload.user_key,
        event_types=payload.event_types,
    ).to_dict()


@router.get("")
def list_subscriptions(
    user_key: str | None = None,
) -> list[dict]:
    return [
        item.to_dict()
        for item in _service.list(user_key=user_key)
    ]


@router.delete("/{subscription_id}")
def disable_subscription(
    subscription_id: str,
) -> dict:
    return {
        "subscription_id": subscription_id,
        "disabled": _service.disable(subscription_id),
    }