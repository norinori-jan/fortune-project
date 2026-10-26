from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FavoriteFortune:
    favorite_id: str
    name: str
    question: str
    system: str
    created_at: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.favorite_id,
            "name": self.name,
            "question": self.question,
            "system": self.system,
            "created_at": self.created_at,
        }
