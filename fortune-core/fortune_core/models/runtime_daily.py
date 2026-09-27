from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeDaily:
    date: str
    theme: str
    title: str
    message: str
    advice: str
    lucky_keywords: tuple[str, ...]
    lucky_number: int
    lucky_direction: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "date": self.date,
            "theme": self.theme,
            "title": self.title,
            "message": self.message,
            "advice": self.advice,
            "lucky_keywords": list(self.lucky_keywords),
            "lucky_number": self.lucky_number,
            "lucky_direction": self.lucky_direction,
        }