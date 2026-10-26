from __future__ import annotations
from dataclasses import dataclass
import hashlib
from typing import Any
@dataclass(frozen=True, slots=True)
class TarotCard:
    number: int
    name: str
    keywords: tuple[str, ...]
    meaning: str

    @property
    def message(self) -> str:
        return self.meaning

    @property
    def advice(self) -> str:
        return f"「{self.keywords[0]}」を意識して過ごしてください。"


@dataclass(frozen=True, slots=True)
class TarotResult:
    question: str
    card: TarotCard
    orientation: str
    message: str
    advice: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "card": {
                "number": self.card.number,
                "name": self.card.name,
                "keywords": list(self.card.keywords),
                "meaning": self.card.meaning,
            },
            "orientation": self.orientation,
            "message": self.message,
            "advice": self.advice,
        }
MAJOR_ARCANA = (
    TarotCard(0, "愚者", ("自由", "始まり", "可能性"), "新しい道へ踏み出す余地があります。"),
    TarotCard(1, "魔術師", ("創造", "行動", "才能"), "持っている力を具体的な行動へ変える時です。"),
    TarotCard(2, "女教皇", ("直感", "知性", "静けさ"), "急いで判断せず、内側の感覚を確認してください。"),
    TarotCard(3, "女帝", ("豊かさ", "育成", "愛情"), "育てているものに時間をかけることで成果につながります。"),
    TarotCard(4, "皇帝", ("秩序", "責任", "基盤"), "ルールと計画を整えることが前進につながります。"),
    TarotCard(5, "法王", ("伝統", "学び", "助言"), "経験者の知恵や既存の方法が役立つ可能性があります。"),
    TarotCard(6, "恋人", ("選択", "調和", "関係"), "自分が大切にしたい価値観を基準に選択してください。"),
    TarotCard(7, "戦車", ("前進", "集中", "決断"), "目的を一つに絞ることで動きやすくなります。"),
    TarotCard(8, "力", ("忍耐", "自制", "勇気"), "強く押すより、落ち着いて扱うことが力になります。"),
    TarotCard(9, "隠者", ("探求", "内省", "知恵"), "一度立ち止まって本質を見直す時間が役立ちます。"),
    TarotCard(10, "運命の輪", ("転機", "流れ", "変化"), "状況の変化を観察し、新しい流れに対応してください。"),
    TarotCard(11, "正義", ("公平", "判断", "均衡"), "感情だけでなく事実と条件を整理してください。"),
    TarotCard(12, "吊るされた男", ("視点", "忍耐", "転換"), "別の角度から見ることで意味が変わる可能性があります。"),
    TarotCard(13, "死神", ("終了", "転換", "再生"), "古い状態を終えることが次の段階につながります。"),
    TarotCard(14, "節制", ("調整", "調和", "循環"), "異なるものを無理なく組み合わせることが鍵になります。"),
    TarotCard(15, "悪魔", ("執着", "欲望", "束縛"), "自分を縛っている習慣や条件を見直してください。"),
    TarotCard(16, "塔", ("変化", "崩壊", "再構築"), "前提が変わる可能性を考えて柔軟に対応してください。"),
    TarotCard(17, "星", ("希望", "理想", "回復"), "目指したい方向を明確にすることが助けになります。"),
    TarotCard(18, "月", ("不確実", "感覚", "幻想"), "情報が揃うまで決めつけず確認することが重要です。"),
    TarotCard(19, "太陽", ("明朗", "活力", "成功"), "物事を明確にし、率直に進めることが力になります。"),
    TarotCard(20, "審判", ("再評価", "決断", "再出発"), "過去を振り返り、次の判断へつなげる時です。"),
    TarotCard(21, "世界", ("完成", "統合", "達成"), "これまでの経験をまとめ、次の段階へ移る準備をしてください。"),
)
class TarotFortuneService:
    def draw(
        self,
        question: str,
        orientation: str = "auto",
    ) -> TarotResult:
        question = question.strip()
        if not question:
            raise ValueError("question must not be empty")
        card = self._select_card(question)
        resolved_orientation = self._orientation(question, orientation)
        message = self._message(card, resolved_orientation)
        advice = self._advice(card, resolved_orientation)
        return TarotResult(
            question=question,
            card=card,
            orientation=resolved_orientation,
            message=message,
            advice=advice,
        )
    @staticmethod
    def _select_card(question: str) -> TarotCard:
        digest = hashlib.sha256(question.encode("utf-8")).digest()
        number = int.from_bytes(digest[:4], "big") % len(MAJOR_ARCANA)
        return MAJOR_ARCANA[number]
    @staticmethod
    def _orientation(question: str, orientation: str) -> str:
        if orientation in {"upright", "reversed"}:
            return orientation
        digest = hashlib.sha256(
            f"orientation:{question}".encode("utf-8")
        ).digest()
        return "upright" if digest[0] % 2 == 0 else "reversed"
    @staticmethod
    def _message(card: TarotCard, orientation: str) -> str:
        if orientation == "upright":
            return card.meaning
        return f"{card.name}のテーマを見直す時です。{card.meaning}"
    @staticmethod
    def _advice(card: TarotCard, orientation: str) -> str:
        if orientation == "upright":
            return f"{card.keywords[0]}を意識し、具体的な一歩を決めてください。"
        return f"{card.keywords[-1]}に偏りすぎていないか、一度確認してください。"