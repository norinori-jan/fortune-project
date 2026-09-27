from __future__ import annotations

from threading import RLock

from fortune_core.models.runtime_preferences import (
    FortuneRuntimePreferences,
)


class FortuneRuntimePreferencesService:
    def __init__(self) -> None:
        self._items: dict[str, FortuneRuntimePreferences] = {}
        self._lock = RLock()

    def get(self, user_key: str) -> FortuneRuntimePreferences:
        with self._lock:
            return self._items.get(
                user_key,
                FortuneRuntimePreferences(user_key=user_key),
            )

    def update(
        self,
        user_key: str,
        *,
        theme: str | None = None,
        language: str | None = None,
        notifications_enabled: bool | None = None,
        daily_enabled: bool | None = None,
        favorite_systems: list[str] | None = None,
    ) -> FortuneRuntimePreferences:
        with self._lock:
            current = self.get(user_key)

            item = FortuneRuntimePreferences(
                user_key=user_key,
                theme=(
                    theme
                    if theme is not None
                    else current.theme
                ),
                language=(
                    language
                    if language is not None
                    else current.language
                ),
                notifications_enabled=(
                    notifications_enabled
                    if notifications_enabled is not None
                    else current.notifications_enabled
                ),
                daily_enabled=(
                    daily_enabled
                    if daily_enabled is not None
                    else current.daily_enabled
                ),
                favorite_systems=(
                    tuple(favorite_systems)
                    if favorite_systems is not None
                    else current.favorite_systems
                ),
                metadata=current.metadata,
            )

            self._items[user_key] = item
            return item