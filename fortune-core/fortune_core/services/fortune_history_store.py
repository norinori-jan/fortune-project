from __future__ import annotations
from datetime import datetime, timezone
from threading import RLock
import hashlib
from fortune_core.models.fortune_history_record import FortuneHistoryRecord
class FortuneHistoryStore:
    def __init__(self, max_items: int = 100) -> None:
        self.max_items = max(1, max_items)
        self._items: list[FortuneHistoryRecord] = []
        self._lock = RLock()
    @staticmethod
    def _make_id(
        question: str,
        system: str,
        created_at: str,
    ) -> str:
        raw = f"{question}|{system}|{created_at}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:20]
    def add(
        self,
        question: str,
        system: str,
        title: str,
        summary: str,
    ) -> FortuneHistoryRecord:
        created_at = datetime.now(timezone.utc).isoformat()
        record = FortuneHistoryRecord(
            record_id=self._make_id(
                question,
                system,
                created_at,
            ),
            question=question,
            system=system,
            title=title,
            summary=summary,
            created_at=created_at,
        )
        with self._lock:
            self._items.insert(0, record)
            del self._items[self.max_items:]
        return record
    def list(self) -> tuple[FortuneHistoryRecord, ...]:
        with self._lock:
            return tuple(self._items)
    def clear(self) -> None:
        with self._lock:
            self._items.clear()