from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeSearchResult:
    key: str
    title: str
    category: str
    score: float
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "category": self.category,
            "score": self.score,
            "metadata": self.metadata,
        }