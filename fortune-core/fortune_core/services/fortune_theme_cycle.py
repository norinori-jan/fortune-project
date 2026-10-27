from __future__ import annotations
from datetime import date
import hashlib
from fortune_core.models.fortune_theme_cycle import (
    FortuneThemeCycle,
    FortuneThemeCycleItem,
)
from fortune_core.services.theme_fortune import ThemeFortuneService
class FortuneThemeCycleService:
    THEMES = (
        "love",
        "work",
        "money",
        "health",
        "general",
    )
    def __init__(self) -> None:
        self.theme_service = ThemeFortuneService()
    def build(
        self,
        question: str,
        period: str = "week",
        target_date: date | None = None,
    ) -> FortuneThemeCycle:
        target_date = target_date or date.today()
        if period == "year":
            period_key = str(target_date.year)
            period_label = "年間テーマ"
        else:
            period_key = target_date.strftime("%Y-W%W")
            period_label = "週間テーマ"
        items: list[FortuneThemeCycleItem] = []
        for theme in self.THEMES:
            result = self.theme_service.divine(question, theme)
            digest = hashlib.sha256(
                f"{question}|{theme}|{period_key}".encode(
                    "utf-8"
                )
            ).digest()
            keywords = tuple(result.keywords)
            if digest[0] % 2 == 0:
                keywords += ("継続",)
            else:
                keywords += ("変化",)
            items.append(
                FortuneThemeCycleItem(
                    theme=theme,
                    title=result.title,
                    message=result.message,
                    advice=(" / ".join(result.advice) if isinstance(result.advice, (list, tuple)) else result.advice),
                    keywords=keywords,
                )
            )
        return FortuneThemeCycle(
            period=period_label,
            period_key=period_key,
            items=tuple(items),
        )
