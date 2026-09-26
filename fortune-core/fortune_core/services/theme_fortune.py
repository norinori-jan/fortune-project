from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from .fortune_themes import FortuneThemeService
from .period_fortune import PeriodFortuneService
from .tarot_fortune import TarotFortuneService
@dataclass(frozen=True, slots=True)
class ThemeFortune:
    question: str
    theme: str
    title: str
    score: int
    message: str
    keywords: list[str]
    advice: list[str]
    tarot: dict
    period: dict
    def to_dict(self) -> dict:
        return {
            "question": self.question,
            "theme": self.theme,
            "title": self.title,
            "score": self.score,
            "message": self.message,
            "keywords": self.keywords,
            "advice": self.advice,
            "tarot": self.tarot,
            "period": self.period,
        }
class ThemeFortuneService:
    def __init__(self) -> None:
        self.themes = FortuneThemeService()
        self.tarot = TarotFortuneService()
        self.period = PeriodFortuneService()
    def divine(
        self,
        question: str,
        theme: str = "general",
    ) -> ThemeFortune:
        question = question.strip()
        if not question:
            raise ValueError("question must not be empty")
        selected = self.themes.get(theme)
        seed = int.from_bytes(
            sha256(
                f"{selected.key}:{question}".encode("utf-8")
            ).digest()[:4],
            "big",
        )
        score = 50 + seed % 51
        tarot = self.tarot.draw(question)
        from datetime import date
        period = self.period.divine(
            date.today(),
            "day",
        )
        keywords = list(
            dict.fromkeys(
                [
                    *selected.keywords,
                    *tarot.card.keywords,
                ]
            )
        )
        advice = list(
            dict.fromkeys(
                [
                    *selected.advice,
                    tarot.advice,
                    period.advice,
                ]
            )
        )
        return ThemeFortune(
            question=question,
            theme=selected.key,
            title=selected.title,
            score=score,
            message=selected.message,
            keywords=keywords,
            advice=advice,
            tarot=tarot.to_dict(),
            period=period.to_dict(),
        )
