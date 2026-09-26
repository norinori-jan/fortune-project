from __future__ import annotations
from .fortune_registry import FortuneProviderRegistry
from ..services.complete_fortune import CompleteFortuneService
from ..services.five_elements import FiveElementService
from ..services.meihua_fortune import MeihuaFortuneService
from ..services.tarot_fortune import TarotFortuneService
from ..services.unified_fortune import UnifiedFortuneService
def create_default_registry() -> FortuneProviderRegistry:
    registry = FortuneProviderRegistry()
    registry.register(
        "unified",
        UnifiedFortuneService(),
        title="総合占い",
        description="質問をもとにした基本的な総合リーディング",
        categories=("general",),
    )
    registry.register(
        "tarot",
        TarotFortuneService(),
        title="タロット",
        description="大アルカナによるカードリーディング",
        categories=("card", "general"),
    )
    registry.register(
        "meihua",
        MeihuaFortuneService(),
        title="梅花易数",
        description="卦と動爻を用いたリーディング",
        categories=("iching", "traditional"),
    )
    registry.register(
        "five-elements",
        FiveElementService(),
        title="五行",
        description="五行バランスによる分析",
        categories=("elements", "general"),
    )
    registry.register(
        "complete",
        CompleteFortuneService(),
        title="総合占術",
        description="複数の新規占術をまとめたリーディング",
        categories=("general", "combined"),
    )
    return registry