from __future__ import annotations

from datetime import datetime, timezone
from threading import RLock
from typing import Any

from fortune_core.models.runtime_history_item import (
    FortuneRuntimeHistoryItem,
)


class FortuneRuntimeHistoryItemService:
    def __init__(
        self,
        max_items: int = 100,
    ) -> None:
        self.max_items = max(1, max_items)
        self._items: list[FortuneRuntimeHistoryItem] = []
        self._lock = RLock()

    def add(
        self,
        *,
        request_id: str,
        user_key: str,
        operation: str,
        theme: str,
        question: str,
        result: dict[str, Any],
    ) -> FortuneRuntimeHistoryItem:
        item = FortuneRuntimeHistoryItem(
            request_id=request_id,
            user_key=user_key,
            operation=operation,
            theme=theme,
            question=question,
            result=result,
            created_at=datetime.now(
                timezone.utc
            ).isoformat(),
        )

        with self._lock:
            self._items.append(item)
            self._items = self._items[-self.max_items:]

        return item

    def list(
        self,
        user_key: str,
        limit: int = 50,
    ) -> list[FortuneRuntimeHistoryItem]:
        with self._lock:
            items = [
                item
                for item in self._items
                if item.user_key == user_key
            ]

        return items[-max(1, limit):]

    def latest(
        self,
        user_key: str,
    ) -> FortuneRuntimeHistoryItem | None:
        items = self.list(user_key, limit=1)
        return items[-1] if items else None