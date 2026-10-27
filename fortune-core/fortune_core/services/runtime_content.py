from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from fortune_core.services.runtime_daily import (
    FortuneRuntimeDailyService,
)
from fortune_core.services.period_views import (
    FortunePeriodViewService,
)


class FortuneRuntimeContentService:
    def __init__(self) -> None:
        self.daily = FortuneRuntimeDailyService()
        self.periods = FortunePeriodViewService()

    def daily_content(
        self,
        user_key: str,
        theme: str = "general",
    ) -> dict[str, Any]:
        return self.daily.get(
            user_key=user_key,
            theme=theme,
        ).to_dict()

    def weekly_content(
        self,
        user_key: str,
        theme: str = "general",
    ) -> list[dict[str, Any]]:
        today = date.today()

        return [
            self.daily.get(
                user_key=user_key,
                theme=theme,
                target_date=today + timedelta(days=index),
            ).to_dict()
            for index in range(7)
        ]

    def period_summary(
        self,
        user_key: str,
        theme: str = "general",
    ) -> list[dict[str, Any]]:
        return [
            self.periods.get(
                user_key=user_key,
                theme=theme,
                period=period,
            ).to_dict()
            for period in (
                "day",
                "month",
                "year",
            )
        ]