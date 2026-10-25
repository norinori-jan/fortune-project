rom __future__ import annotations
from collections import deque
from datetime import datetime, timezone
from hashlib import sha256
from threading import Lock
from typing import Any
from fortune_core.models.fortune_history import FortuneHistoryItem
class FortuneHistoryService:
    def __init__(self, max_items: int = 100) -> None:
        self._items: deque[FortuneHistoryItem] = deque(
            maxlen=max_items
        )
        self._lock = Lock()
    def add(
        self,
        system: str,
        question: str,
        result: dict[str, Any],
    ) -> FortuneHistoryItem:
        created_at = datetime.now(timezone.utc)
        raw_id = (
            f"{system}:{question}:{created_at.isoformat()}"
        )
        item = FortuneHistoryItem(
            id=sha256(raw_id.encode("utf-8")).hexdigest()[:16],
            created_at=created_at,
            system=system,
            question=question,
            result=result,
        )
        with self._lock:
            self._items.appendleft(item)
        return item
    def list(
        self,
        limit: int = 20,
    ) -> list[FortuneHistoryItem]:
        limit = max(1, min(limit, len(self._items)))
        with self._lock:
            return list(self._items)[:limit]
    def clear(self) -> None:
        with self._lock:
            self._items.clear()