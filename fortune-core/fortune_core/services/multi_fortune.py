from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .complete_fortune import CompleteFortuneService
from .five_elements import FiveElementService
from .theme_fortune import ThemeFortuneService
@dataclass(frozen=True, slots=True)
class MultiFortune:
    question: str
    theme: str
    systems: list[dict[str, Any]]
    overall: str
    keywords: list[str]
    advice: list[str]
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "theme": self.theme,
            "systems": self.systems,
            "overall": self.overall,
            "keywords": self.keywords,
            "advice": self.advice,
        }
class MultiFortuneService:
    def __init__(self) -> None:
        self.complete = CompleteFortuneService()
        self.theme = ThemeFortuneService()
        self.elements = FiveElementService()
    def divine(
        self,
        question: str,
        theme: str = "general",
    ) -> MultiFortune:
        complete = self.complete.divine(question)
        themed = self.theme.divine(
            question,
            theme,
        )
        elements = self.elements.analyze(question)
        systems = [
            {
                "system": "complete",
                "result": complete.to_dict(),
            },
            {
                "system": "theme",
                "result": themed.to_dict(),
            },
            {
                "system": "five-elements",
                "result": elements.to_dict(),
            },
        ]
        keywords = list(
            dict.fromkeys(
                [
                    *complete.keywords,
                    *themed.keywords,
                    elements.dominant(),
                    elements.lacking(),
                ]
            )
        )
        advice = list(
            dict.fromkeys(
                [
                    *complete.advice,
                    *themed.advice,
                ]
            )
        )
        overall = (
            f"{themed.title}を中心に、"
            f"{themed.message}"
        )
        return MultiFortune(
            question=question,
            theme=themed.theme,
            systems=systems,
            overall=overall,
            keywords=keywords,
            advice=advice,
        )
