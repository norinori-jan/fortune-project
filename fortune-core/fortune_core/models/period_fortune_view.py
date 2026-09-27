from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortunePeriodView:
    period: str
    title: str
    score: int
    message: str
    advice: str
    keywords: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "period": self.period,
            "title": self.title,
            "score": self.score,
            "message": self.message,
            "advice": self.advice,
            "keywords": list(self.keywords),
        }