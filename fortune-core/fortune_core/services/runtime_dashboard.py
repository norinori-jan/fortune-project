from __future__ import annotations

from fortune_core.models.runtime_dashboard import (
    FortuneRuntimeDashboard,
)
from fortune_core.services.runtime_daily import (
    FortuneRuntimeDailyService,
)
from fortune_core.services.runtime_favorites import (
    FortuneRuntimeFavoriteService,
)
from fortune_core.services.runtime_history_items import (
    FortuneRuntimeHistoryItemService,
)
from fortune_core.services.runtime_user import (
    FortuneRuntimeUserService,
)


class FortuneRuntimeDashboardService:
    def __init__(self) -> None:
        self.user = FortuneRuntimeUserService()
        self.daily = FortuneRuntimeDailyService()
        self.favorites = FortuneRuntimeFavoriteService()
        self.history = FortuneRuntimeHistoryItemService()

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> FortuneRuntimeDashboard:
        return FortuneRuntimeDashboard(
            user_key=user_key,
            theme=theme,
            daily=self.daily.get(
                user_key=user_key,
                theme=theme,
            ).to_dict(),
            profile=self.user.profile(user_key),
            summary=self.user.summary_for(user_key),
            recommendations=tuple(
                self.user.recommendations_for(
                    user_key,
                    themes=[theme],
                )
            ),
            favorites=tuple(
                item.to_dict()
                for item in self.favorites.list(user_key)
            ),
            recent_history=tuple(
                item.to_dict()
                for item in self.history.list(
                    user_key,
                    limit=10,
                )
            ),
        )