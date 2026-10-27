from __future__ import annotations

from typing import Any
from uuid import uuid4

from fortune_core.models.runtime_delivery import (
    FortuneRuntimeDelivery,
)
from fortune_core.models.runtime_event_subscription import (
    FortuneRuntimeEventSubscription,
)


class FortuneRuntimeDeliveryService:
    def __init__(self) -> None:
        self._deliveries: list[FortuneRuntimeDelivery] = []

    def build(
        self,
        subscription: FortuneRuntimeEventSubscription,
        event_type: str,
        payload: dict[str, Any],
    ) -> FortuneRuntimeDelivery:
        accepted = subscription.accepts(event_type)

        item = FortuneRuntimeDelivery(
            delivery_id=uuid4().hex,
            subscription_id=subscription.subscription_id,
            event_type=event_type,
            status="queued" if accepted else "skipped",
            payload=payload,
        )

        self._deliveries.append(item)

        return item

    def list(
        self,
        subscription_id: str | None = None,
    ) -> list[FortuneRuntimeDelivery]:
        if subscription_id is None:
            return list(self._deliveries)

        return [
            item
            for item in self._deliveries
            if item.subscription_id == subscription_id
        ]