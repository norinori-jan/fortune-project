from __future__ import annotations
from fortune_core.models.fortune_compare import (
    FortuneCompareItem,
    FortuneComparison,
)
from fortune_core.services.complete_fortune import (
    CompleteFortuneService,
)
class FortuneCompareService:
    def __init__(self) -> None:
        self.complete_service = CompleteFortuneService()
    def build(
        self,
        question: str,
    ) -> FortuneComparison:
        result = self.complete_service.divine(question)
        items = (
            FortuneCompareItem(
                system="unified",
                title=result.unified.title,
                message=result.unified.message,
                advice=result.unified.advice,
            ),
            FortuneCompareItem(
                system="tarot",
                title=result.tarot.card.name,
                message=result.tarot.card.message,
                advice=result.tarot.card.advice,
            ),
            FortuneCompareItem(
                system="meihua",
                title=result.meihua.title,
                message=result.meihua.message,
                advice=result.meihua.advice,
            ),
        )
        return FortuneComparison(
            question=question,
            items=items,
        )
