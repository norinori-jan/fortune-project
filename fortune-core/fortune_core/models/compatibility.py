from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class CompatibilityResult:
    score: int
    title: str
    message: str
    advice: str
    keywords: tuple[str, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "score": self.score,
            "title": self.title,
            "message": self.message,
            "advice": self.advice,
            "keywords": list(self.keywords),
        }