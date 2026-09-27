from __future__ import annotations

from fortune_core.models.hub_page import FortuneHubPage
from fortune_core.services.hub_widgets import (
    FortuneHubWidgetService,
)
from fortune_core.services.runtime_daily import (
    FortuneRuntimeDailyService,
)
from fortune_core.services.runtime_recommendation import (
    FortuneRuntimeRecommendationService,
)
from fortune_core.services.runtime_user import (
    FortuneRuntimeUserService,
)


class FortuneHubPageService:
    def __init__(self) -> None:
        self.widgets = FortuneHubWidgetService()
        self.daily = FortuneRuntimeDailyService()
        self.recommendation = (
            FortuneRuntimeRecommendationService()
        )
        self.user = FortuneRuntimeUserService()

    def home(
        self,
        user_key: str,
        theme: str = "general",
    ) -> FortuneHubPage:
        daily = self.daily.get(
            user_key=user_key,
            theme=theme,
        )

        recommendation = self.recommendation.recommend(
            user_key=user_key,
            theme=theme,
        )

        widget_list = self.widgets.build_navigation(theme)

        widget_list.insert(
            0,
            self._daily_widget(daily.to_dict()),
        )

        widget_list.insert(
            1,
            self._recommendation_widget(
                recommendation.to_dict()
            ),
        )

        return FortuneHubPage(
            page_key="home",
            title="Fortune Hub",
            theme=theme,
            widgets=tuple(
                widget.to_dict()
                for widget in widget_list
            ),
            metadata={
                "user_key": user_key,
                "section_count": len(widget_list),
            },
        )

    def _daily_widget(self, data: dict) -> object:
        from fortune_core.models.hub_widget import (
            FortuneHubWidget,
        )

        return FortuneHubWidget(
            key="daily",
            title="今日の運勢",
            widget_type="daily-fortune",
            priority=0,
            data=data,
            actions=("open_daily",),
        )

    def _recommendation_widget(self, data: dict) -> object:
        from fortune_core.models.hub_widget import (
            FortuneHubWidget,
        )

        return FortuneHubWidget(
            key="recommendation",
            title="おすすめ",
            widget_type="recommendation",
            priority=0,
            data=data,
            actions=("start_recommended",),
        )