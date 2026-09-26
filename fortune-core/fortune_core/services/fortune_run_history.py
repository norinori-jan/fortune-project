from __future__ import annotations
from collections import deque
from datetime import datetime, timezone
from threading import RLock
from ..models.fortune_pipeline import FortunePipelineResult
from ..models.fortune_run_record import FortuneRunRecord
class FortuneRunHistoryService:
    def __init__(self, max_items: int = 100) -> None:
        self._items: deque[FortuneRunRecord] = deque(
            maxlen=max_items
        )
        self._lock = RLock()
    def record(
        self,
        result: FortunePipelineResult,
    ) -> FortuneRunRecord:
        record = FortuneRunRecord(
            execution_id=result.execution_id,
            theme=result.context.theme,
            question=result.context.question,
            created_at=datetime.now(timezone.utc),
            systems=tuple(
                item.system
                for item in result.results
            ),
            result_count=len(result.results),
        )
        with self._lock:
            self._items.appendleft(record)
        return record
    def list(
        self,
        limit: int = 20,
    ) -> list[FortuneRunRecord]:
        with self._lock:
            return list(self._items)[:limit]
    def get(
        self,
        execution_id: str,
    ) -> FortuneRunRecord | None:
        with self._lock:
            for item in self._items:
                if item.execution_id == execution_id:
                    return item
        return None
