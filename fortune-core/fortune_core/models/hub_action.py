from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class HubAction:
    key: str
    title: str
    description: str
    category: str
    priority: int
    metadata: dict[str, Any] | None = None
    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "priority": self.priority,
            "metadata": self.metadata or {},
        }
