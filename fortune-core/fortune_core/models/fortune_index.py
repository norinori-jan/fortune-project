from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class FortuneIndexEntry:
    result_id: str
    system: str
    theme: str
    title: str
    keywords: tuple[str, ...] = ()
    text: str = ""
    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "system": self.system,
            "theme": self.theme,
            "title": self.title,
            "keywords": list(self.keywords),
            "text": self.text,
        }
@dataclass(frozen=True)
class FortuneSearchResult:
    query: str
    items: tuple[FortuneIndexEntry, ...] = ()
    total: int = 0
    def to_dict(self) -> dict[str, Any]:
        return {
            "query": self.query,
            "total": self.total,
            "items": [
                item.to_dict()
                for item in self.items
            ],
        }