from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneMessage:
    message_id: str
    category: str
    title: str
    message: str
    keyword: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.message_id,
            "category": self.category,
            "title": self.title,
            "message": self.message,
            "keyword": self.keyword,
        }