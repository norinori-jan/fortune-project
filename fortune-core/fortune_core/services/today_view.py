from __future__ import annotations

from fortune_core.models.today_view import FortuneTodayView
from fortune_core.services.runtime_daily import (
    FortuneRuntimeDailyService,
)


class FortuneTodayViewService:
    def __init__(self) -> None:
        self.daily = FortuneRuntimeDailyService()

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> FortuneTodayView:
        item = self.daily.get(
            user_key=user_key,
            theme=theme,
        )

        return FortuneTodayView(
            date=item.date,
            theme=item.theme,
            title=item.title,
            score=item.score,
            message=item.message,
            advice=item.advice,
            lucky_keywords=tuple(
                item.lucky_keywords
            ),
            lucky_number=item.lucky_number,
            lucky_direction=item.lucky_direction,
            metadata={
                "source": "runtime-daily",
            },
        )