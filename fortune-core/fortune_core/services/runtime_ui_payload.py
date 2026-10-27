from __future__ import annotations

from fortune_core.models.runtime_ui_payload import (
    FortuneRuntimeUiPayload,
)
from fortune_core.services.hub_page import (
    FortuneHubPageService,
)
from fortune_core.services.question_guide import (
    FortuneQuestionGuideService,
)
from fortune_core.services.runtime_daily import (
    FortuneRuntimeDailyService,
)
from fortune_core.services.runtime_recommendation import (
    FortuneRuntimeRecommendationService,
)


class FortuneRuntimeUiPayloadService:
    def __init__(self) -> None:
        self.page = FortuneHubPageService()
        self.daily = FortuneRuntimeDailyService()
        self.guide = FortuneQuestionGuideService()
        self.recommendation = (
            FortuneRuntimeRecommendationService()
        )

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> FortuneRuntimeUiPayload:
        return FortuneRuntimeUiPayload(
            user_key=user_key,
            theme=theme,
            page=self.page.home(
                user_key=user_key,
                theme=theme,
            ).to_dict(),
            daily=self.daily.get(
                user_key=user_key,
                theme=theme,
            ).to_dict(),
            question_guide=self.guide.get(
                theme
            ).to_dict(),
            recommendations=tuple(
                item.to_dict()
                for item in self.recommendation.list(
                    user_key=user_key,
                    themes=[theme],
                )
            ),
            metadata={
                "surface": "fortune-hub",
                "api_version": "1.0.0",
            },
        )