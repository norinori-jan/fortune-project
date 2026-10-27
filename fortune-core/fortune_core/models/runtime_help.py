from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeHelp:
    key: str
    title: str
    description: str
    example_question: str
    recommended_systems: tuple[str, ...]
    recommended_operation: str
    keywords: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "description": self.description,
            "example_question": self.example_question,
            "recommended_systems": list(
                self.recommended_systems
            ),
            "recommended_operation": (
                self.recommended_operation
            ),
            "keywords": list(self.keywords),
        }