from __future__ import annotations
from collections import deque
from threading import RLock
from fortune_core.models.runtime_request_record import (
    FortuneRuntimeRequestRecord,
)
class FortuneRuntimeHistoryService:
    def __init__(self, max_items: int = 500) -> None:
        self.max_items = max(1, max_items)
        self._items: deque[FortuneRuntimeRequestRecord] = deque(
            maxlen=self.max_items
        )
        self._lock = RLock()
    def add(
        self,
        item: FortuneRuntimeRequestRecord,
    ) -> FortuneRuntimeRequestRecord:
        with self._lock:
            self._items.append(item)
        return item
    def list(
        self,
        user_key: str | None = None,
        operation: str | None = None,
    ) -> list[FortuneRuntimeRequestRecord]:
        with self._lock:
            items = list(self._items)
        if user_key is not None:
            items = [
                item for item in items
                if item.user_key == user_key
            ]
        if operation is not None:
            items = [
                item for item in items
                if item.operation == operation
            ]
        return items
    def latest(
        self,
        user_key: str,
    ) -> FortuneRuntimeRequestRecord | None:
        items = self.list(user_key=user_key)
        if not items:
            return None
        return items[-1]
    def clear(self) -> None:
        with self._lock:
            self._items.clear()