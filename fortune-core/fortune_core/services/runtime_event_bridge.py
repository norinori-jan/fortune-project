from __future__ import annotations

from typing import Any

from fortune_core.models.hub_event import HubEvent
from fortune_core.services.runtime_delivery import (
    FortuneRuntimeDeliveryService,
)
from fortune_core.services.runtime_event_subscriptions import (
    FortuneRuntimeEventSubscriptionService,
)


class FortuneRuntimeEventBridge:
    def __init__(
        self,
        subscriptions: FortuneRuntimeEventSubscriptionService | None = None,
        delivery: FortuneRuntimeDeliveryService | None = None,
    ) -> None:
        self.subscriptions = (
            subscriptions
            or FortuneRuntimeEventSubscriptionService()
        )
        self.delivery = (
            delivery
            or FortuneRuntimeDeliveryService()
        )

    def publish(
        self,
        event: HubEvent,
    ) -> list[dict[str, Any]]:
        result = []

        for subscription in self.subscriptions.list(
            user_key=event.user_key
        ):
            item = self.delivery.build(
                subscription,
                event.event_type,
                event.to_dict(),
            )

            if item.status != "skipped":
                result.append(item.to_dict())

        return result