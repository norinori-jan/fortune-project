from __future__ import annotations
from fortune_core.models.runtime_recommendation import (
    FortuneRuntimeRecommendation,
)
from fortune_core.services.theme_router import (
    FortuneThemeRouterService,
)
class FortuneRuntimeRecommendationService:
    def __init__(
        self,
        router: FortuneThemeRouterService | None = None,
    ) -> None:
        self.router = router or FortuneThemeRouterService()
    def recommend(
        self,
        user_key: str,
        theme: str,
    ) -> FortuneRuntimeRecommendation:
        route = self.router.get(theme)
        return FortuneRuntimeRecommendation(
            user_key=user_key,
            theme=route.theme,
            system=route.primary_system,
            operation=route.recommended_operation,
            reason=(
                f"{route.theme}テーマでは"
                f"{route.primary_system}を中心に"
                "確認できる構成です。"
            ),
            keywords=route.keywords,
        )
    def list(
        self,
        user_key: str,
        themes: list[str] | None = None,
    ) -> list[FortuneRuntimeRecommendation]:
        selected = themes or [
            "general",
            "love",
            "work",
            "money",
            "health",
        ]
        return [
            self.recommend(user_key, theme)
            for theme in selected
        ]