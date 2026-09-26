from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneProfile:
    profile_id: str
    nickname: str
    birth_date: str | None
    favorite_system: str
    favorite_theme: str
    keywords: tuple[str, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.profile_id,
            "nickname": self.nickname,
            "birth_date": self.birth_date,
            "favorite_system": self.favorite_system,
            "favorite_theme": self.favorite_theme,
            "keywords": list(self.keywords),
        }