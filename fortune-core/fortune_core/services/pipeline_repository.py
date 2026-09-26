from .pipeline_store import FortunePipelineStore
__all__ = ["FortunePipelineStore"]

165. fortune-core/fortune_core/models/fortune_feed.py

from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneFeedItem:
    key: str
    category: str
    title: str
    message: str
    system: str | None = None
    theme: str = "general"
    priority: int = 0
    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "category": self.category,
            "title": self.title,
            "message": self.message,
            "system": self.system,
            "theme": self.theme,
            "priority": self.priority,
        }
@dataclass(frozen=True)
class FortuneFeed:
    theme: str
    items: tuple[FortuneFeedItem, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "items": [
                item.to_dict()
                for item in self.items
            ],
        }