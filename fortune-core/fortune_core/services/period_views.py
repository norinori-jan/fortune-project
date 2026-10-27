from __future__ import annotations

from fortune_core.models.period_fortune_view import (
    FortunePeriodView,
)
from fortune_core.services.period_fortune import (
    PeriodFortuneService,
)


class FortunePeriodViewService:
    def __init__(
        self,
        service: PeriodFortuneService | None = None,
    ) -> None:
        self.service = service or PeriodFortuneService()

    def get(
        self,
        user_key: str,
        theme: str,
        period: str,
    ) -> FortunePeriodView:
        # PeriodFortuneService は日付と期間で決まる。user_key・theme で値が変わるよう日付に混ぜる
        import hashlib
        from datetime import date, timedelta
        shift = int(hashlib.sha256(f"{user_key}|{theme}".encode("utf-8")).hexdigest()[:4], 16) % 365
        result = self.service.divine(
            date.today() - timedelta(days=shift),
            period,
        )

        return FortunePeriodView(
            period=period,
            title=result.title,
            score=result.score,
            message=result.message,
            advice=result.advice,
            keywords=(theme, period),
        )