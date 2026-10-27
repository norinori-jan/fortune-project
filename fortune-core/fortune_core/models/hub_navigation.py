from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class HubNavigationItem:
    key: str
    title: str
    path: str
    description: str
    system: str | None = None
    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "path": self.path,
            "description": self.description,
            "system": self.system,
        }
@dataclass(frozen=True)
class HubNavigation:
    items: tuple[HubNavigationItem, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "items": [
                item.to_dict()
                for item in self.items
            ]
        }