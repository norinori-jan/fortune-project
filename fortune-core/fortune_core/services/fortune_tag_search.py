from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneTag:
    key: str
    label: str
    category: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "label": self.label,
            "category": self.category,
        }
class FortuneTagService:
    TAGS = (
        FortuneTag("forward", "前進", "action"),
        FortuneTag("growth", "成長", "action"),
        FortuneTag("change", "変化", "action"),
        FortuneTag("stability", "安定", "state"),
        FortuneTag("harmony", "調和", "relationship"),
        FortuneTag("discovery", "発見", "insight"),
        FortuneTag("整理", "整理", "action"),
        FortuneTag("直感", "直感", "insight"),
        FortuneTag("love", "恋愛", "theme"),
        FortuneTag("work", "仕事", "theme"),
        FortuneTag("money", "お金", "theme"),
        FortuneTag("health", "生活", "theme"),
    )
    def all(self) -> tuple[FortuneTag, ...]:
        return self.TAGS
    def find(self, query: str) -> tuple[FortuneTag, ...]:
        query = query.strip().lower()
        if not query:
            return self.TAGS
        return tuple(
            item
            for item in self.TAGS
            if query in item.key.lower()
            or query in item.label.lower()
            or query in item.category.lower()
        )
