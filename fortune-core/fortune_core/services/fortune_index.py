from __future__ import annotations
from threading import RLock
from ..models.fortune_index import (
    FortuneIndexEntry,
    FortuneSearchResult,
)
from ..models.fortune_result import FortuneResult
class FortuneIndexService:
    def __init__(self) -> None:
        self._entries: dict[str, FortuneIndexEntry] = {}
        self._lock = RLock()
    def add(self, result: FortuneResult) -> FortuneIndexEntry:
        entry = FortuneIndexEntry(
            result_id=result.result_id,
            system=result.system,
            theme=result.theme,
            title=result.title,
            keywords=result.keywords,
            text=(
                f"{result.title} "
                f"{result.summary} "
                f"{result.message}"
            ),
        )
        with self._lock:
            self._entries[result.result_id] = entry
        return entry
    def add_many(
        self,
        results: list[FortuneResult],
    ) -> list[FortuneIndexEntry]:
        return [
            self.add(result)
            for result in results
        ]
    def get(
        self,
        result_id: str,
    ) -> FortuneIndexEntry | None:
        with self._lock:
            return self._entries.get(result_id)
    def search(
        self,
        query: str,
        *,
        theme: str | None = None,
        system: str | None = None,
        limit: int = 20,
    ) -> FortuneSearchResult:
        normalized = query.strip().lower()
        if not normalized:
            return FortuneSearchResult(
                query=query,
                items=(),
                total=0,
            )
        with self._lock:
            entries = list(self._entries.values())
        matched: list[FortuneIndexEntry] = []
        for entry in entries:
            if theme and entry.theme != theme:
                continue
            if system and entry.system != system:
                continue
            searchable = " ".join(
                (
                    entry.title,
                    entry.text,
                    entry.theme,
                    entry.system,
                    *entry.keywords,
                )
            ).lower()
            if normalized in searchable:
                matched.append(entry)
        matched.sort(
            key=lambda item: (
                item.theme,
                item.system,
                item.title,
            )
        )
        return FortuneSearchResult(
            query=query,
            items=tuple(matched[:limit]),
            total=len(matched),
        )
    def clear(self) -> None:
        with self._lock:
            self._entries.clear()
    def size(self) -> int:
        with self._lock:
            return len(self._entries)