from __future__ import annotations

from fortune_core.models.system_selector import (
    FortuneSystemOption,
)


class FortuneSystemSelectorService:
    OPTIONS = (
        FortuneSystemOption(
            key="unified",
            title="総合占い",
            description="複数の要素をまとめて見る",
            operation="divine",
            themes=("general", "love", "work", "money", "health"),
        ),
        FortuneSystemOption(
            key="tarot",
            title="タロット",
            description="カードから現在のテーマを読む",
            operation="draw",
            themes=("general", "love", "work", "money", "health"),
        ),
        FortuneSystemOption(
            key="meihua",
            title="梅花易数",
            description="卦の組み合わせから流れを見る",
            operation="divine",
            themes=("general", "love", "work", "money"),
        ),
        FortuneSystemOption(
            key="five-elements",
            title="五行",
            description="五行バランスからテーマを整理する",
            operation="analyze",
            themes=("general", "work", "money", "health"),
        ),
    )

    def list(
        self,
        theme: str = "general",
    ) -> list[FortuneSystemOption]:
        return [
            option
            for option in self.OPTIONS
            if theme in option.themes
        ]

    def get(
        self,
        key: str,
    ) -> FortuneSystemOption | None:
        return next(
            (
                option
                for option in self.OPTIONS
                if option.key == key
            ),
            None,
        )