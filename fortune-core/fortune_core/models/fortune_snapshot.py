from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneSnapshot:
    snapshot_id: str
    question: str
    system: str
    theme: str
    date_key: str
    title: str
    message: str
    advice: str
    keywords: tuple[str, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.snapshot_id,
            "question": self.question,
            "system": self.system,
            "theme": self.theme,
            "date": self.date_key,
            "title": self.title,
            "message": self.message,
            "advice": self.advice,
            "keywords": list(self.keywords),
        }
