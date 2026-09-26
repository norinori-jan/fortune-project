from __future__ import annotations
from datetime import date
from .five_elements import FiveElementService
from .meihua_fortune import MeihuaFortuneService
from .shichu_profile import ShichuProfileService
from .tarot_fortune import TarotFortuneService
from .complete_fortune import CompleteFortuneService
class FortuneFacade:
    """
    新規占術の入口。
    個々のエンジンを直接呼び出さず、
    上位アプリケーションから統一的に利用するための層。
    """
    def __init__(self) -> None:
        self.complete = CompleteFortuneService()
        self.tarot = TarotFortuneService()
        self.meihua = MeihuaFortuneService()
        self.elements = FiveElementService()
        self.shichu = ShichuProfileService()
    def complete_fortune(self, question: str):
        return self.complete.divine(question)
    def tarot_fortune(
        self,
        question: str,
        orientation: str = "auto",
    ):
        return self.tarot.draw(
            question,
            orientation,
        )
    def meihua_fortune(self, question: str):
        return self.meihua.divine(question)
    def element_analysis(self, text: str):
        return self.elements.analyze(text)
    def shichu_profile(self, birth_date: date):
        return self.shichu.create(birth_date)