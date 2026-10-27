from __future__ import annotations
from collections import deque
from threading import RLock
from ..models.fortune_pipeline import FortunePipelineResult
class FortunePipelineStore:
    """
    Pipeline結果の短期保管領域。
    永続DBではなく、後から差し替え可能な境界として設計。
    """
    def __init__(self, max_items: int = 100) -> None:
        self._items: deque[FortunePipelineResult] = deque(
            maxlen=max_items
        )
        self._lock = RLock()
    def add(
        self,
        result: FortunePipelineResult,
    ) -> FortunePipelineResult:
        with self._lock:
            self._items.appendleft(result)
        return result
    def get(
        self,
        execution_id: str,
    ) -> FortunePipelineResult | None:
        with self._lock:
            for item in self._items:
                if item.execution_id == execution_id:
                    return item
        return None
    def list(
        self,
        limit: int = 20,
    ) -> list[FortunePipelineResult]:
        with self._lock:
            return list(self._items)[:limit]
    def clear(self) -> None:
        with self._lock:
            self._items.clear()
    def size(self) -> int:
        with self._lock:
            return len(self._items)