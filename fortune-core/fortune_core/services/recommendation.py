from __future__ import annotations
import hashlib
from dataclasses import dataclass
@dataclass(frozen=True)
class FortuneRecommendation:
    system: str
    title: str
    reason: str
    question: str
    theme: str
    def to_dict(self) -> dict[str, str]:
        return {
            "system": self.system,
            "title": self.title,
            "reason": self.reason,
            "question": self.question,
            "theme": self.theme,
        }
class FortuneRecommendationService:
    """
    質問・テーマから最初に試す占術候補を決定する。
    評価ではなく、用途別のルーティングを担当する。
    """
    SYSTEMS = {
        "love": (
            (
                "tarot",
                "タロット",
                "今の気持ちや関係性の流れを見る質問に向いています。",
                "今の関係で意識するとよいことは？",
            ),
            (
                "compatibility",
                "相性占い",
                "二人の関係性を整理する質問に向いています。",
                "二人の関係で大切にしたいことは？",
            ),
            (
                "meihua",
                "梅花易数",
                "今起きている変化の流れを考える質問に使えます。",
                "この関係はこれからどう変化する？",
            ),
        ),
        "work": (
            (
                "iching",
                "易経",
                "状況の変化と行動の方向を考える質問に向いています。",
                "今の仕事で意識すべき流れは？",
            ),
            (
                "tarot",
                "タロット",
                "選択肢や現在のテーマを整理する質問に使えます。",
                "今の仕事で見落としていることは？",
            ),
            (
                "five-elements",
                "五行",
                "バランスや不足している要素を考える入口になります。",
                "今の自分に必要なバランスは？",
            ),
        ),
        "money": (
            (
                "iching",
                "易経",
                "変化の中での判断や姿勢を考える質問に向いています。",
                "お金について今意識するべきことは？",
            ),
            (
                "five-elements",
                "五行",
                "生活や行動のバランスを整理する入口になります。",
                "今の生活で整えたい部分は？",
            ),
            (
                "tarot",
                "タロット",
                "現在のテーマを多角的に見る質問に使えます。",
                "今のお金のテーマで意識することは？",
            ),
        ),
        "health": (
            (
                "five-elements",
                "五行",
                "生活全体のバランスを考える入口になります。",
                "今の生活で整えたいバランスは？",
            ),
            (
                "tarot",
                "タロット",
                "現在の心構えや生活テーマを整理する質問に使えます。",
                "今の自分を整えるために意識することは？",
            ),
            (
                "iching",
                "易経",
                "変化への向き合い方を考える質問に向いています。",
                "今の生活で見直したい流れは？",
            ),
        ),
        "general": (
            (
                "iching",
                "易経",
                "全体的な流れを考える質問に向いています。",
                "今の自分に必要なことは？",
            ),
            (
                "tarot",
                "タロット",
                "現在のテーマを多角的に見る質問に使えます。",
                "今の自分が意識するとよいことは？",
            ),
            (
                "meihua",
                "梅花易数",
                "目の前の変化や流れを考える質問に使えます。",
                "今起きていることから何を学べる？",
            ),
        ),
    }
    def recommend(
        self,
        *,
        question: str = "",
        theme: str = "general",
        limit: int = 3,
    ) -> list[FortuneRecommendation]:
        normalized_theme = theme if theme in self.SYSTEMS else "general"
        items = list(self.SYSTEMS[normalized_theme])
        seed = hashlib.sha256(
            f"{normalized_theme}|{question}".encode("utf-8")
        ).digest()
        offset = seed[0] % len(items)
        rotated = items[offset:] + items[:offset]
        return [
            FortuneRecommendation(
                system=system,
                title=title,
                reason=reason,
                question=suggested_question,
                theme=normalized_theme,
            )
            for system, title, reason, suggested_question in rotated[:limit]
        ]
