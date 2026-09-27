from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeFavorite:
    favorite_id: str
    user_key: str
    title: str
    system: str
    theme: str
    question: str
    result: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "favorite_id": self.favorite_id,
            "user_key": self.user_key,
            "title": self.title,
            "system": self.system,
            "theme": self.theme,
            "question": self.question,
            "result": self.result,
            "created_at": self.created_at,
        }