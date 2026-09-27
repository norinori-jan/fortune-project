from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneQuestionGuide:
    theme: str
    title: str
    examples: tuple[str, ...]
    tips: tuple[str, ...]
    recommended_systems: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "title": self.title,
            "examples": list(self.examples),
            "tips": list(self.tips),
            "recommended_systems": list(
                self.recommended_systems
            ),
        }