from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneCatalogItem:
    key: str
    name: str
    description: str
    category: str
    available: bool = True
    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "name": self.name,
            "description": self.description,
            "category": self.category,
            "available": self.available,
        }
