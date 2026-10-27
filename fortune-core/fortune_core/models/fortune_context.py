from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneContext:
    user_key: str | None = None
    birth_date: str | None = None
    question: str = ""
    theme: str = "general"
    locale: str = "ja-JP"
    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "birth_date": self.birth_date,
            "question": self.question,
            "theme": self.theme,
            "locale": self.locale,
        }
