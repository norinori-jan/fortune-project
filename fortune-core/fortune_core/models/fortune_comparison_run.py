from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .fortune_provider_result import FortuneProviderResult
@dataclass(frozen=True)
class FortuneComparisonRun:
    theme: str
    question: str
    items: tuple[FortuneProviderResult, ...]
    common_keywords: tuple[str, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "question": self.question,
            "items": [
                item.to_dict()
                for item in self.items
            ],
            "common_keywords": list(
                self.common_keywords
            ),
        }
