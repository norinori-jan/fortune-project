from __future__ import annotations
from datetime import datetime, timezone
import hashlib
from threading import RLock
from fortune_core.models.favorite import FavoriteFortune
class FavoriteFortuneService:
    def __init__(self) -> None:
        self._items: dict[str, FavoriteFortune] = {}
        self._lock = RLock()
    @staticmethod
    def _id(name: str, question: str, system: str) -> str:
        raw = f"{name}|{question}|{system}"
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    def add(
        self,
        name: str,
        question: str,
        system: str,
    ) -> FavoriteFortune:
        favorite_id = self._id(name, question, system)
        item = FavoriteFortune(
            favorite_id=favorite_id,
            name=name,
            question=question,
            system=system,
            created_at=datetime.now(timezone.utc).isoformat(),
        )
        with self._lock:
            self._items[favorite_id] = item
        return item
    def get(self, favorite_id: str) -> FavoriteFortune | None:
        with self._lock:
            return self._items.get(favorite_id)
    def list(self) -> tuple[FavoriteFortune, ...]:
        with self._lock:
            return tuple(self._items.values())
    def remove(self, favorite_id: str) -> bool:
        with self._lock:
            return self._items.pop(favorite_id, None) is not None