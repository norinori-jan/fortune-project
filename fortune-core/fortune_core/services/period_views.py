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
        result = self.service.get(
            user_key=user_key,
            theme=theme,
            period=period,
        )

        return FortunePeriodView(
            period=period,
            title=result.title,
            score=result.score,
            message=result.message,
            advice=result.advice,
            keywords=tuple(result.keywords),
        )