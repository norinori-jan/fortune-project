from __future__ import annotations

from threading import RLock
from uuid import uuid4

from fortune_core.models.runtime_event_subscription import (
    FortuneRuntimeEventSubscription,
)


class FortuneRuntimeEventSubscriptionService:
    def __init__(self) -> None:
        self._items: dict[
            str,
            FortuneRuntimeEventSubscription,
        ] = {}
        self._lock = RLock()

    def create(
        self,
        user_key: str,
        event_types: list[str] | None = None,
    ) -> FortuneRuntimeEventSubscription:
        subscription_id = uuid4().hex

        item = FortuneRuntimeEventSubscription(
            subscription_id=subscription_id,
            user_key=user_key,
            event_types=tuple(event_types or ()),
        )

        with self._lock:
            self._items[subscription_id] = item

        return item

    def get(
        self,
        subscription_id: str,
    ) -> FortuneRuntimeEventSubscription | None:
        with self._lock:
            return self._items.get(subscription_id)

    def list(
        self,
        user_key: str | None = None,
    ) -> list[FortuneRuntimeEventSubscription]:
        with self._lock:
            items = list(self._items.values())

        if user_key is not None:
            items = [
                item
                for item in items
                if item.user_key == user_key
            ]

        return items

    def disable(
        self,
        subscription_id: str,
    ) -> bool:
        with self._lock:
            current = self._items.get(subscription_id)

            if current is None:
                return False

            self._items[subscription_id] = (
                FortuneRuntimeEventSubscription(
                    subscription_id=current.subscription_id,
                    user_key=current.user_key,
                    event_types=current.event_types,
                    enabled=False,
                    metadata=current.metadata,
                )
            )

            return True