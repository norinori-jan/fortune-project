from __future__ import annotations
from datetime import date
import hashlib
from fortune_core.models.fortune_bundle import (
    FortuneBundle,
    FortuneDetailCard,
)
from fortune_core.services.complete_fortune import CompleteFortuneService
from fortune_core.services.five_elements import FiveElementService
from fortune_core.services.fortune_summary import FortuneSummaryService
class FortuneBundleService:
    def __init__(self) -> None:
        self.complete_service = CompleteFortuneService()
        self.element_service = FiveElementService()
        self.summary_service = FortuneSummaryService()
    @staticmethod
    def _score(seed: str) -> int:
        digest = hashlib.sha256(seed.encode("utf-8")).digest()
        return 50 + digest[0] % 51
    def build(
        self,
        question: str,
        target_date: date | None = None,
    ) -> FortuneBundle:
        target_date = target_date or date.today()
        complete = self.complete_service.divine(question)
        cards: list[FortuneDetailCard] = []
        unified = complete.unified
        cards.append(
            FortuneDetailCard(
                system="unified",
                title="総合占い",
                subtitle="全体の流れ",
                message=unified.message,
                advice=unified.advice,
                keywords=tuple(unified.keywords),
            )
        )
        tarot = complete.tarot
        cards.append(
            FortuneDetailCard(
                system="tarot",
                title=tarot.card.name,
                subtitle=tarot.orientation,
                message=tarot.card.message,
                advice=tarot.card.advice,
                keywords=tuple(tarot.card.keywords),
            )
        )
        meihua = complete.meihua
        cards.append(
            FortuneDetailCard(
                system="meihua",
                title=meihua.title,
                subtitle=meihua.trigram_name,
                message=meihua.message,
                advice=meihua.advice,
                keywords=tuple(meihua.keywords),
            )
        )
        element = self.element_service.analyze(
            question=question,
            target_date=target_date,
        )
        cards.append(
            FortuneDetailCard(
                system="five-elements",
                title="五行バランス",
                subtitle=element.dominant,
                message=element.message,
                advice=element.advice,
                keywords=tuple(element.keywords),
            )
        )
        scores = [
            self._score(f"{question}|{card.system}|{target_date.isoformat()}")
            for card in cards
        ]
        summary = self.summary_service.build(scores)
        summary_card = FortuneDetailCard(
            system="summary",
            title=summary.headline,
            subtitle="総合ガイド",
            message=summary.message,
            advice=summary.advice,
            keywords=summary.tags,
        )
        return FortuneBundle(
            question=question,
            date_key=target_date.isoformat(),
            summary=summary_card,
            cards=tuple(cards),
        )