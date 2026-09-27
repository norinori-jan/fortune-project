from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from uuid import uuid4
from typing import Any

from fortune_core.models.runtime_favorite import (
    FortuneRuntimeFavorite,
)


class FortuneRuntimeFavoriteService:
    def __init__(self) -> None:
        self._items: dict[str, FortuneRuntimeFavorite] = {}
        self._lock = RLock()

    def add(
        self,
        user_key: str,
        *,
        title: str,
        system: str,
        theme: str,
        question: str,
        result: dict[str, Any],
    ) -> FortuneRuntimeFavorite:
        item = FortuneRuntimeFavorite(
            favorite_id=uuid4().hex,
            user_key=user_key,
            title=title,
            system=system,
            theme=theme,
            question=question,
            result=result,
            created_at=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        with self._lock:
            self._items[item.favorite_id] = item

        return item

    def get(
        self,
        favorite_id: str,
    ) -> FortuneRuntimeFavorite | None:
        with self._lock:
            return self._items.get(favorite_id)

    def list(
        self,
        user_key: str,
    ) -> list[FortuneRuntimeFavorite]:
        with self._lock:
            return [
                item
                for item in self._items.values()
                if item.user_key == user_key
            ]

    def remove(
        self,
        favorite_id: str,
        user_key: str | None = None,
    ) -> bool:
        with self._lock:
            item = self._items.get(favorite_id)

            if item is None:
                return False

            if (
                user_key is not None
                and item.user_key != user_key
            ):
                return False

            del self._items[favorite_id]
            return True