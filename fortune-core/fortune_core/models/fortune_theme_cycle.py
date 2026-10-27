from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneThemeCycleItem:
    theme: str
    title: str
    message: str
    advice: str
    keywords: tuple[str, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "title": self.title,
            "message": self.message,
            "advice": self.advice,
            "keywords": list(self.keywords),
        }
@dataclass(frozen=True)
class FortuneThemeCycle:
    period: str
    period_key: str
    items: tuple[FortuneThemeCycleItem, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "period": self.period,
            "period_key": self.period_key,
            "items": [item.to_dict() for item in self.items],
        }