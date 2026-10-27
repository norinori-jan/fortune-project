from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeDiscoveryItem:
    key: str
    title: str
    description: str
    category: str
    operation: str
    theme: str = "general"
    keywords: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "operation": self.operation,
            "theme": self.theme,
            "keywords": list(self.keywords),
        }