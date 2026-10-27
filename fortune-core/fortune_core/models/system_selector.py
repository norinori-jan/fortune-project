from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneSystemOption:
    key: str
    title: str
    description: str
    operation: str
    themes: tuple[str, ...]
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "description": self.description,
            "operation": self.operation,
            "themes": list(self.themes),
            "enabled": self.enabled,
        }