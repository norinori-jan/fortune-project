from __future__ import annotations

from threading import RLock

from fortune_core.models.runtime_notification import (
    FortuneRuntimeNotificationPreference,
)


class FortuneRuntimeNotificationService:
    def __init__(self) -> None:
        self._items: dict[
            str,
            FortuneRuntimeNotificationPreference,
        ] = {}
        self._lock = RLock()

    def get(
        self,
        user_key: str,
    ) -> FortuneRuntimeNotificationPreference:
        with self._lock:
            return self._items.get(
                user_key,
                FortuneRuntimeNotificationPreference(
                    user_key=user_key
                ),
            )

    def update(
        self,
        user_key: str,
        *,
        enabled: bool | None = None,
        morning: bool | None = None,
        afternoon: bool | None = None,
        evening: bool | None = None,
    ) -> FortuneRuntimeNotificationPreference:
        with self._lock:
            current = self.get(user_key)

            item = FortuneRuntimeNotificationPreference(
                user_key=user_key,
                enabled=(
                    enabled
                    if enabled is not None
                    else current.enabled
                ),
                morning=(
                    morning
                    if morning is not None
                    else current.morning
                ),
                afternoon=(
                    afternoon
                    if afternoon is not None
                    else current.afternoon
                ),
                evening=(
                    evening
                    if evening is not None
                    else current.evening
                ),
            )

            self._items[user_key] = item
            return item