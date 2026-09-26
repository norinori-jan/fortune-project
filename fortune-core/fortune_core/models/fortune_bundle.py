from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneDetailCard:
    system: str
    title: str
    subtitle: str
    message: str
    advice: str
    keywords: tuple[str, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "system": self.system,
            "title": self.title,
            "subtitle": self.subtitle,
            "message": self.message,
            "advice": self.advice,
            "keywords": list(self.keywords),
        }
@dataclass(frozen=True)
class FortuneBundle:
    question: str
    date_key: str
    summary: FortuneDetailCard
    cards: tuple[FortuneDetailCard, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "date": self.date_key,
            "summary": self.summary.to_dict(),
            "cards": [card.to_dict() for card in self.cards],
        }