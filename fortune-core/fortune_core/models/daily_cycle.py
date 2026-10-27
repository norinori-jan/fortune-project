from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class DailyCycleItem:
    period: str
    title: str
    score: int
    message: str
    advice: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "period": self.period,
            "title": self.title,
            "score": self.score,
            "message": self.message,
            "advice": self.advice,
        }
@dataclass(frozen=True)
class DailyCycle:
    date_key: str
    items: tuple[DailyCycleItem, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date_key,
            "items": [item.to_dict() for item in self.items],
        }