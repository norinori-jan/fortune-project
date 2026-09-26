from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class FortuneServiceManifest:
    name: str
    version: str
    category: str
    operations: tuple[str, ...]
    themes: tuple[str, ...] = ()
    description: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "category": self.category,
            "operations": list(self.operations),
            "themes": list(self.themes),
            "description": self.description,
            "metadata": self.metadata,
        }