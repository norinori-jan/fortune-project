from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneCalendarEntry:
    date_key: str
    score: int
    title: str
    message: str
    keyword: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date_key,
            "score": self.score,
            "title": self.title,
            "message": self.message,
            "keyword": self.keyword,
        }