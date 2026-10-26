from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from fortune_core.models import FortuneItem, UnifiedFortune
from .meihua_fortune import MeihuaFortuneService
from .tarot_fortune import TarotFortuneService
from .unified_fortune import UnifiedFortuneService
@dataclass(frozen=True)
class UnifiedView:
    """画面・カード用に、総合の結果を 1 枚分（文字列の助言）にした見え方。"""
    message: str
    advice: str
    keywords: tuple[str, ...]
    overall: str = ""
    title: str = "総合占い"

    def to_dict(self) -> dict[str, Any]:
        return {"message": self.message, "advice": self.advice,
                "keywords": list(self.keywords), "overall": self.overall}


@dataclass(frozen=True)
class CompleteFortuneResult:
    """総合占い（complete）の結果：総合・タロット・梅花を別々に持つ形（案A）。

    総合（UnifiedFortune）の項目 question/theme/overall/message/items/keywords/advice は
    そのまま同名で読める。
    """
    base: UnifiedFortune
    unified: UnifiedView
    tarot: Any
    meihua: Any

    question = property(lambda s: s.base.question)
    theme = property(lambda s: s.base.theme)
    overall = property(lambda s: s.base.overall)
    message = property(lambda s: s.base.message)
    items = property(lambda s: s.base.items)
    keywords = property(lambda s: s.base.keywords)
    advice = property(lambda s: s.base.advice)

    def to_dict(self) -> dict[str, Any]:
        d = self.base.to_dict()
        d["unified"] = self.unified.to_dict()
        d["tarot"] = self.tarot.to_dict()
        d["meihua"] = self.meihua.to_dict()
        return d


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
    def divine(self, question: str, theme: str = "general") -> CompleteFortuneResult:
        base = self.unified.divine(question, theme)
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
        merged = UnifiedFortune(
            question=question,
            theme=base.theme,
            overall=base.overall,
            message=base.message,
            items=items,
            keywords=keywords,
            advice=advice,
        )
        return CompleteFortuneResult(
            base=merged,
            unified=UnifiedView(
                message=base.message,
                advice=" / ".join(base.advice),
                keywords=tuple(base.keywords),
                overall=base.overall,
            ),
            tarot=tarot,
            meihua=meihua,
        )
