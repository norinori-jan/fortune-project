from __future__ import annotations
from datetime import date
from ..models.fortune_feed import (
    FortuneFeed,
    FortuneFeedItem,
)
from .hub_action import FortuneHubActionService
from .hub_insight import FortuneHubInsightService
from .recommendation import FortuneRecommendationService
class FortuneFeedService:
    def __init__(self) -> None:
        self.insights = FortuneHubInsightService()
        self.actions = FortuneHubActionService()
        self.recommendations = FortuneRecommendationService()
    def build(
        self,
        *,
        theme: str = "general",
        question: str = "",
        target_date: date | None = None,
        limit: int = 10,
    ) -> FortuneFeed:
        current_date = target_date or date.today()
        items: list[FortuneFeedItem] = []
        insight_result = self.insights.generate(
            theme=theme,
            target_date=current_date,
            limit=3,
        )
        for index, item in enumerate(
            insight_result.insights,
            start=1,
        ):
            items.append(
                FortuneFeedItem(
                    key=f"insight-{index}",
                    category="insight",
                    title=item.title,
                    message=item.message,
                    theme=theme,
                    priority=index,
                )
            )
        action_result = self.actions.generate(
            theme=theme,
            target_date=current_date,
            limit=3,
        )
        for item in action_result:
            items.append(
                FortuneFeedItem(
                    key=f"action-{item.key}",
                    category="action",
                    title=item.title,
                    message=item.description,
                    theme=theme,
                    priority=item.priority,
                )
            )
        recommendations = self.recommendations.recommend(
            question=question,
            theme=theme,
            limit=3,
        )
        for index, item in enumerate(
            recommendations,
            start=1,
        ):
            items.append(
                FortuneFeedItem(
                    key=f"recommendation-{item.system}",
                    category="recommendation",
                    title=item.title,
                    message=item.reason,
                    system=item.system,
                    theme=theme,
                    priority=index,
                )
            )
        return FortuneFeed(
            theme=theme,
            items=tuple(items[:limit]),
        )
