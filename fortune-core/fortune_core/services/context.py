from __future__ import annotations
from ..models.fortune_context import FortuneContext
class FortuneContextService:
    VALID_THEMES = {
        "general",
        "love",
        "work",
        "money",
        "health",
    }
    def create(
        self,
        *,
        user_key: str | None = None,
        birth_date: str | None = None,
        question: str = "",
        theme: str = "general",
        locale: str = "ja-JP",
    ) -> FortuneContext:
        normalized_theme = (
            theme
            if theme in self.VALID_THEMES
            else "general"
        )
        return FortuneContext(
            user_key=user_key,
            birth_date=birth_date,
            question=question.strip(),
            theme=normalized_theme,
            locale=locale,
        )
