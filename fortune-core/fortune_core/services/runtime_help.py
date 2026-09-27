from __future__ import annotations

from fortune_core.models.runtime_help import FortuneRuntimeHelp


class FortuneRuntimeHelpService:
    ITEMS = (
        FortuneRuntimeHelp(
            key="love",
            title="恋愛について占う",
            description="恋愛や人間関係について質問します。",
            example_question="今の関係をどう進めるとよい？",
            recommended_systems=("tarot", "unified", "meihua"),
            recommended_operation="quick",
            keywords=("恋愛", "関係", "出会い"),
        ),
        FortuneRuntimeHelp(
            key="work",
            title="仕事について占う",
            description="仕事やキャリアについて質問します。",
            example_question="今の仕事で意識するとよいことは？",
            recommended_systems=(
                "unified",
                "five-elements",
                "tarot",
            ),
            recommended_operation="quick",
            keywords=("仕事", "キャリア", "挑戦"),
        ),
        FortuneRuntimeHelp(
            key="money",
            title="お金について占う",
            description="金運やお金の流れについて質問します。",
            example_question="今月のお金の使い方で意識することは？",
            recommended_systems=(
                "five-elements",
                "unified",
                "tarot",
            ),
            recommended_operation="quick",
            keywords=("金運", "お金", "収支"),
        ),
        FortuneRuntimeHelp(
            key="general",
            title="総合運を見る",
            description="複数の占術を組み合わせて全体を確認します。",
            example_question="今の自分に必要なメッセージは？",
            recommended_systems=("unified", "tarot", "meihua"),
            recommended_operation="home",
            keywords=("総合", "全体", "メッセージ"),
        ),
    )

    def list(self) -> list[FortuneRuntimeHelp]:
        return list(self.ITEMS)

    def get(
        self,
        key: str,
    ) -> FortuneRuntimeHelp | None:
        for item in self.ITEMS:
            if item.key == key:
                return item

        return None