from __future__ import annotations
from collections import OrderedDict
from threading import RLock
from typing import Any
class FortuneHubCache:
    def __init__(self, max_items: int = 256) -> None:
        self.max_items = max(1, max_items)
        self._items: OrderedDict[str, dict[str, Any]] = OrderedDict()
        self._lock = RLock()
    def get(self, key: str) -> dict[str, Any] | None:
        with self._lock:
            value = self._items.get(key)
            if value is None:
                return None
            self._items.move_to_end(key)
            return dict(value)
    def set(self, key: str, value: dict[str, Any]) -> None:
        with self._lock:
            self._items[key] = dict(value)
            self._items.move_to_end(key)
            while len(self._items) > self.max_items:
                self._items.popitem(last=False)
    def delete(self, key: str) -> bool:
        with self._lock:
            return self._items.pop(key, None) is not None
    def clear(self) -> None:
        with self._lock:
            self._items.clear()
    def size(self) -> int:
        with self._lock:
            return len(self._items)
