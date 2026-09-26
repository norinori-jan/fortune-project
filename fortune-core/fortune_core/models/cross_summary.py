from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class CrossSummary:
    theme: str
    headline: str
    message: str
    common_keywords: tuple[str, ...]
    systems: tuple[str, ...]
    scores: dict[str, int] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "headline": self.headline,
            "message": self.message,
            "common_keywords": list(self.common_keywords),
            "systems": list(self.systems),
            "scores": dict(self.scores),
        }
