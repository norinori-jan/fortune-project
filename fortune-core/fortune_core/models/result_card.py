from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneResultCard:
    result_id: str
    title: str
    system: str
    theme: str
    headline: str
    score: int | None
    message: str
    advice: str
    keywords: tuple[str, ...]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "title": self.title,
            "system": self.system,
            "theme": self.theme,
            "headline": self.headline,
            "score": self.score,
            "message": self.message,
            "advice": self.advice,
            "keywords": list(self.keywords),
            "metadata": self.metadata,
        }