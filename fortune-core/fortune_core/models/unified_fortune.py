from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True, slots=True)
class FortuneItem:
    system: str
    title: str
    summary: str
    details: dict[str, Any] = field(default_factory=dict)
@dataclass(frozen=True, slots=True)
class UnifiedFortune:
    question: str
    theme: str
    overall: str
    message: str
    items: list[FortuneItem] = field(default_factory=list)
    keywords: list[str] = field(default_factory=list)
    advice: list[str] = field(default_factory=list)
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "theme": self.theme,
            "overall": self.overall,
            "message": self.message,
            "items": [
                {
                    "system": item.system,
                    "title": item.title,
                    "summary": item.summary,
                    "details": item.details,
                }
                for item in self.items
            ],
            "keywords": self.keywords,
            "advice": self.advice,
        }
