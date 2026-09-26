from __future__ import annotations
from fortune_core.models import FortuneItem, UnifiedFortune
from .meihua_fortune import MeihuaFortuneService
from .tarot_fortune import TarotFortuneService
from .unified_fortune import UnifiedFortuneService
class CompleteFortuneService:
    """
    新規占術だけで構成する総合占い。
    既存の I Ching / Tarot / 梅花実装を変更せず、
    後からアダプターを追加できる構造にする。
    """
    def __init__(self) -> None:
        self.unified = UnifiedFortuneService()
        self.tarot = TarotFortuneService()
        self.meihua = MeihuaFortuneService()
    def divine(self, question: str) -> UnifiedFortune:
        base = self.unified.divine(question)
        tarot = self.tarot.draw(question)
        meihua = self.meihua.divine(question)
        items = [
            *base.items,
            FortuneItem(
                system="tarot",
                title=tarot.card.name,
                summary=tarot.message,
                details=tarot.to_dict(),
            ),
            FortuneItem(
                system="meihua",
                title=f"{meihua.upper}{meihua.lower}",
                summary=meihua.message,
                details=meihua.to_dict(),
            ),
        ]
        keywords = list(
            dict.fromkeys(
                [
                    *base.keywords,
                    *tarot.card.keywords,
                    meihua.upper,
                    meihua.lower,
                ]
            )
        )
        advice = list(
            dict.fromkeys(
                [
                    *base.advice,
                    tarot.advice,
                    meihua.advice,
                ]
            )
        )
        return UnifiedFortune(
            question=question,
            theme=base.theme,
            overall=base.overall,
            message=base.message,
            items=items,
            keywords=keywords,
            advice=advice,
        )