from __future__ import annotations

import hashlib

from fortune_core.models.today_view import FortuneTodayView
from fortune_core.services.runtime_daily import (
    FortuneRuntimeDailyService,
)


class FortuneTodayViewService:
    def __init__(self) -> None:
        self.daily = FortuneRuntimeDailyService()

    @staticmethod
    def _score(user_key: str, day: str, theme: str) -> int:
        """他の運勢カードと同じ決め方（sha256 → 50〜100）。"""
        digest = hashlib.sha256(f"{user_key}|{day}|{theme}".encode("utf-8")).digest()
        return 50 + digest[0] % 51

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
            score=getattr(item, "score", None) or self._score(user_key, item.date, item.theme),
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