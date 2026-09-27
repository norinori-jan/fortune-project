from __future__ import annotations

from fortune_core.models.question_guide import (
    FortuneQuestionGuide,
)


class FortuneQuestionGuideService:
    GUIDES = {
        "general": FortuneQuestionGuide(
            theme="general",
            title="総合運について質問",
            examples=(
                "今の自分に必要なメッセージは？",
                "これからの流れを知りたい",
                "今意識するとよいことは？",
            ),
            tips=(
                "知りたい期間を入れる",
                "具体的なテーマを一つに絞る",
            ),
            recommended_systems=(
                "unified",
                "tarot",
                "meihua",
            ),
        ),
        "love": FortuneQuestionGuide(
            theme="love",
            title="恋愛について質問",
            examples=(
                "今の関係で意識するとよいことは？",
                "相手との距離をどう考える？",
                "新しい出会いに向けて何を整える？",
            ),
            tips=(
                "相手をコントロールする質問より自分の行動を聞く",
                "現在の状況を短く書く",
            ),
            recommended_systems=(
                "tarot",
                "unified",
                "meihua",
            ),
        ),
        "work": FortuneQuestionGuide(
            theme="work",
            title="仕事について質問",
            examples=(
                "今の仕事で意識することは？",
                "次の一歩を決めるヒントは？",
                "仕事上の課題をどう整理する？",
            ),
            tips=(
                "現在の状況を具体的にする",
                "行動につながる質問にする",
            ),
            recommended_systems=(
                "unified",
                "five-elements",
                "tarot",
            ),
        ),
        "money": FortuneQuestionGuide(
            theme="money",
            title="金運について質問",
            examples=(
                "今月のお金の使い方で意識することは？",
                "収支を整えるヒントは？",
                "今のお金の流れをどう捉える？",
            ),
            tips=(
                "具体的な期間を書く",
                "実際の判断材料と占いを混同しない",
            ),
            recommended_systems=(
                "five-elements",
                "unified",
                "tarot",
            ),
        ),
        "health": FortuneQuestionGuide(
            theme="health",
            title="健康テーマについて質問",
            examples=(
                "生活リズムで意識することは？",
                "休息について考えるヒントは？",
                "今月整えたい習慣は？",
            ),
            tips=(
                "生活上のテーマとして質問する",
                "医療上の判断は専門家に確認する",
            ),
            recommended_systems=(
                "five-elements",
                "unified",
                "meihua",
            ),
        ),
    }

    def get(
        self,
        theme: str,
    ) -> FortuneQuestionGuide:
        return self.GUIDES.get(
            theme,
            self.GUIDES["general"],
        )

    def list(self) -> list[FortuneQuestionGuide]:
        return list(self.GUIDES.values())