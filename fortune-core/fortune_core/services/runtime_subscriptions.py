from __future__ import annotations
from threading import RLock
from fortune_core.models.runtime_subscription import (
    FortuneRuntimeSubscription,
)
class FortuneRuntimeSubscriptionService:
    def __init__(self) -> None:
        self._items: dict[str, FortuneRuntimeSubscription] = {}
        self._lock = RLock()
    def subscribe(
        self,
        subscription_id: str,
        event_type: str,
    ) -> FortuneRuntimeSubscription:
        item = FortuneRuntimeSubscription(
            subscription_id=subscription_id,
            event_type=event_type,
            active=True,
        )
        with self._lock:
            self._items[subscription_id] = item
        return item
    def unsubscribe(self, subscription_id: str) -> bool:
        with self._lock:
            item = self._items.get(subscription_id)
            if item is None:
                return False
            self._items[subscription_id] = FortuneRuntimeSubscription(
                subscription_id=item.subscription_id,
                event_type=item.event_type,
                active=False,
            )
            return True
    def get(
        self,
        subscription_id: str,
    ) -> FortuneRuntimeSubscription | None:
        with self._lock:
            return self._items.get(subscription_id)
    def list(
        self,
        active_only: bool = False,
    ) -> list[FortuneRuntimeSubscription]:
        with self._lock:
            items = list(self._items.values())
        if active_only:
            items = [item for item in items if item.active]
        return items
