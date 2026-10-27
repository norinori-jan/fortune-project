from __future__ import annotations

from typing import Any

from fortune_core.services.runtime_daily import (
    FortuneRuntimeDailyService,
)
from fortune_core.services.runtime_discovery import (
    FortuneRuntimeDiscoveryService,
)
from fortune_core.services.runtime_recommendation import (
    FortuneRuntimeRecommendationService,
)


class FortuneRuntimeFeedService:
    def __init__(self) -> None:
        self.daily = FortuneRuntimeDailyService()
        self.discovery = FortuneRuntimeDiscoveryService()
        self.recommendation = (
            FortuneRuntimeRecommendationService()
        )

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> dict[str, Any]:
        daily = self.daily.get(
            user_key=user_key,
            theme=theme,
        )

        recommendation = self.recommendation.recommend(
            user_key=user_key,
            theme=theme,
        )

        discovery = self.discovery.list(
            theme=theme
        )

        return {
            "user_key": user_key,
            "theme": theme,
            "daily": daily.to_dict(),
            "recommendation": recommendation.to_dict(),
            "discovery": [
                item.to_dict()
                for item in discovery
            ],
        }