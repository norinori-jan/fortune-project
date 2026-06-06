"""
tarot_engine.py
===============
fortune-core タロットエンジン
大アルカナ22枚のシャッフル・ドロー・スプレッドロジック

Author : Nori (norinori-jan)
Version: 1.0.0
Compatible: major.json v1.0.0 / registry_a.json / FORTUNE_REGISTRY アーキテクチャ
"""

import json
import random
import os
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from enum import Enum


# ────────────────────────────────────────────
#  定数・Enum
# ────────────────────────────────────────────

class Orientation(str, Enum):
    UPRIGHT  = "upright"   # 正位置
    REVERSED = "reversed"  # 逆位置


class SpreadType(str, Enum):
    ONE_ORACLE  = "one_oracle"   # ワンオラクル（1枚）
    THREE_CARD  = "three_card"   # スリーカード（過去・現在・未来）
    CELTIC_MINI = "celtic_mini"  # ケルティッククロス簡易版（5枚）
    YES_NO      = "yes_no"       # YES/NO占い（1枚）
    DAILY       = "daily"        # 今日の一枚

# スプレッドのポジション定義
SPREAD_POSITIONS: dict[str, list[str]] = {
    SpreadType.ONE_ORACLE : ["現在の状況"],
    SpreadType.THREE_CARD : ["過去", "現在", "未来"],
    SpreadType.CELTIC_MINI: ["現在の状況", "課題・障害", "顕在意識", "潜在意識", "結果"],
    SpreadType.YES_NO     : ["答え"],
    SpreadType.DAILY      : ["今日のメッセージ"],
}


# ────────────────────────────────────────────
#  データクラス
# ────────────────────────────────────────────

@dataclass
class DrawnCard:
    """1枚ドローした結果"""
    position_label : str            # スプレッド上の位置名
    position_index : int            # 0始まりの位置インデックス
    card_id        : int            # major.json の id
    name_ja        : str
    name_en        : str
    number         : str
    symbol         : str
    orientation    : Orientation
    keywords       : list[str]
    meaning        : str
    element        : str
    planet         : str
    fortune_prompt_hint: str

    # YES/NO 用 (オプション)
    yes_no_answer  : Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "position_label"     : self.position_label,
            "position_index"     : self.position_index,
            "card_id"            : self.card_id,
            "name_ja"            : self.name_ja,
            "name_en"            : self.name_en,
            "number"             : self.number,
            "symbol"             : self.symbol,
            "orientation"        : self.orientation.value,
            "orientation_ja"     : "正位置" if self.orientation == Orientation.UPRIGHT else "逆位置",
            "keywords"           : self.keywords,
            "meaning"            : self.meaning,
            "element"            : self.element,
            "planet"             : self.planet,
            "fortune_prompt_hint": self.fortune_prompt_hint,
            "yes_no_answer"      : self.yes_no_answer,
        }


@dataclass
class SpreadResult:
    """スプレッド全体の結果"""
    spread_type  : SpreadType
    spread_label : str
    drawn_at     : str                      # ISO8601
    cards        : list[DrawnCard] = field(default_factory=list)
    question     : Optional[str]   = None  # ユーザーの質問文

    def to_dict(self) -> dict:
        return {
            "spread_type"  : self.spread_type.value,
            "spread_label" : self.spread_label,
            "drawn_at"     : self.drawn_at,
            "question"     : self.question,
            "cards"        : [c.to_dict() for c in self.cards],
        }

    def to_prompt_context(self) -> str:
        """AI プロンプトに渡す文脈文字列を生成"""
        lines = [
            f"【スプレッド】{self.spread_label}",
            f"【質問】{self.question or '（指定なし）'}",
            "",
        ]
        for c in self.cards:
            ori = "正位置" if c.orientation == Orientation.UPRIGHT else "逆位置"
            kw  = "・".join(c.keywords)
            lines += [
                f"■ {c.position_label}：{c.name_ja}（{c.name_en}）{ori}",
                f"  キーワード：{kw}",
                f"  意味：{c.meaning}",
                "",
            ]
        return "\n".join(lines)


# ────────────────────────────────────────────
#  コアエンジン
# ────────────────────────────────────────────

class TarotEngine:
    """
    タロットエンジン本体

    使い方:
        engine = TarotEngine()                          # major.json 自動検出
        result = engine.draw(SpreadType.THREE_CARD)     # スリーカード
        print(result.to_prompt_context())               # AI プロンプト用テキスト
        print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    """

    def __init__(self, json_path: Optional[str] = None):
        if json_path is None:
            # __file__ と同じディレクトリ、または cwd を自動検索
            candidates = [
                os.path.join(os.path.dirname(__file__), "major.json"),
                os.path.join(os.getcwd(), "major.json"),
            ]
            json_path = next((p for p in candidates if os.path.exists(p)), None)
            if json_path is None:
                raise FileNotFoundError(
                    "major.json が見つかりません。パスを明示してください: TarotEngine('path/to/major.json')"
                )

        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)

        self._meta  = data["meta"]
        self._cards = data["cards"]          # list[dict]  22枚
        self._deck  = list(self._cards)      # シャッフル用コピー

        print(f"[TarotEngine] {"大アルカナタロット"} v{self._meta['version']} loaded — {len(self._cards)} cards")

    # ── パブリック API ──────────────────────────

    def shuffle(self) -> None:
        """デッキをシャッフルする（Fisher-Yates）"""
        random.shuffle(self._deck)

    def draw(
        self,
        spread_type : SpreadType = SpreadType.ONE_ORACLE,
        question    : Optional[str] = None,
        auto_shuffle: bool = True,
    ) -> SpreadResult:
        """
        指定スプレッドでカードを引く。

        Parameters
        ----------
        spread_type  : どのスプレッドで引くか
        question     : 占いたい質問（任意）
        auto_shuffle : 毎回自動シャッフルするか（デフォルト True）

        Returns
        -------
        SpreadResult
        """
        if auto_shuffle:
            self.shuffle()

        positions = SPREAD_POSITIONS[spread_type]
        n         = len(positions)

        # デッキから n 枚重複なしで抽出
        picked = random.sample(self._deck, n)

        drawn_cards: list[DrawnCard] = []
        for i, (pos_label, raw_card) in enumerate(zip(positions, picked)):
            orientation = self._roll_orientation()
            dc = self._build_drawn_card(raw_card, pos_label, i, orientation)

            # YES/NO 判定
            if spread_type in (SpreadType.YES_NO, SpreadType.ONE_ORACLE):
                dc.yes_no_answer = self._evaluate_yes_no(raw_card, orientation)

            drawn_cards.append(dc)

        spread_label = self._spread_label(spread_type)
        result = SpreadResult(
            spread_type  = spread_type,
            spread_label = spread_label,
            drawn_at     = datetime.now().isoformat(timespec="seconds"),
            cards        = drawn_cards,
            question     = question,
        )
        return result

    def draw_one(self, question: Optional[str] = None) -> SpreadResult:
        """ワンオラクル（1枚引き）ショートカット"""
        return self.draw(SpreadType.ONE_ORACLE, question=question)

    def draw_three(self, question: Optional[str] = None) -> SpreadResult:
        """スリーカード（過去・現在・未来）ショートカット"""
        return self.draw(SpreadType.THREE_CARD, question=question)

    def draw_yes_no(self, question: Optional[str] = None) -> SpreadResult:
        """YES/NO 占いショートカット"""
        return self.draw(SpreadType.YES_NO, question=question)

    def draw_daily(self) -> SpreadResult:
        """今日の一枚ショートカット"""
        return self.draw(SpreadType.DAILY)

    def draw_celtic_mini(self, question: Optional[str] = None) -> SpreadResult:
        """ケルティッククロス簡易版（5枚）ショートカット"""
        return self.draw(SpreadType.CELTIC_MINI, question=question)

    # ── registry_a.json / FORTUNE_REGISTRY 連携 ──

    def to_registry_entry(self, result: SpreadResult) -> dict:
        """
        FORTUNE_REGISTRY に登録できる形式に変換する。
        registry_a.json の tarot セクションへの追記用。
        """
        return {
            "type"       : "tarot_reading",
            "spread"     : result.spread_type.value,
            "question"   : result.question,
            "drawn_at"   : result.drawn_at,
            "cards"      : [c.to_dict() for c in result.cards],
            "prompt_ctx" : result.to_prompt_context(),
        }

    # ── プライベートメソッド ──────────────────

    @staticmethod
    def _roll_orientation() -> Orientation:
        """50/50 でランダムに正位置 or 逆位置を返す"""
        return Orientation.UPRIGHT if random.random() < 0.5 else Orientation.REVERSED

    @staticmethod
    def _build_drawn_card(
        raw: dict,
        position_label: str,
        position_index: int,
        orientation: Orientation,
    ) -> DrawnCard:
        """raw dict → DrawnCard"""
        if orientation == Orientation.UPRIGHT:
            keywords = raw["upright"]["keywords"]
            meaning  = raw["upright"]["action_advice"]
        else:
            keywords = raw["reversed"]["keywords"]
            meaning  = raw["reversed"]["action_advice"]

        return DrawnCard(
            position_label     = position_label,
            position_index     = position_index,
            card_id            = raw["id"],
            name_ja            = raw["name_ja"],
            name_en            = raw["name_en"],
            number             = raw["number"],
            symbol             = raw.get("symbol", ""),
            orientation        = orientation,
            keywords           = keywords,
            meaning            = meaning,
            element            = raw.get("element", ""),
            planet             = raw.get("planet", ""),
            fortune_prompt_hint= raw.get("fortune_prompt_hint", ""),
        )

    @staticmethod
    def _evaluate_yes_no(raw: dict, orientation: Orientation) -> str:
        """
        YES/NO 判定ロジック。
        正位置の「肯定的」カードは YES 寄り、逆位置・難しいカードは NO 寄り。
        """
        # 本質的に「肯定」傾向の強いカード id
        YES_IDS  = {0, 1, 3, 4, 6, 7, 8, 10, 11, 17, 19, 21}
        NO_IDS   = {12, 13, 15, 16, 18}

        card_id = raw["id"]

        if orientation == Orientation.UPRIGHT:
            if card_id in YES_IDS:
                return "YES"
            elif card_id in NO_IDS:
                return "MAYBE_NO"
            else:
                return "MAYBE_YES"
        else:  # REVERSED
            if card_id in YES_IDS:
                return "MAYBE_NO"
            elif card_id in NO_IDS:
                return "NO"
            else:
                return "MAYBE_NO"

    @staticmethod
    def _spread_label(spread_type: SpreadType) -> str:
        labels = {
            SpreadType.ONE_ORACLE : "ワンオラクル",
            SpreadType.THREE_CARD : "スリーカード（過去・現在・未来）",
            SpreadType.CELTIC_MINI: "ケルティッククロス（簡易5枚）",
            SpreadType.YES_NO     : "YES/NO占い",
            SpreadType.DAILY      : "今日の一枚",
        }
        return labels.get(spread_type, spread_type.value)


# ────────────────────────────────────────────
#  CLI デモ（python tarot_engine.py で実行）
# ────────────────────────────────────────────

def _pretty_print(result: SpreadResult) -> None:
    print("\n" + "═" * 52)
    print(f"  ✨ {result.spread_label}")
    print(f"  🕐 {result.drawn_at}")
    if result.question:
        print(f"  ❓ {result.question}")
    print("═" * 52)
    for c in result.cards:
        ori_ja = "正位置 ▲" if c.orientation == Orientation.UPRIGHT else "逆位置 ▽"
        print(f"\n  【{c.position_label}】")
        print(f"   {c.symbol}  {c.name_ja} / {c.name_en}  {ori_ja}")
        print(f"   🔑 {' ・ '.join(c.keywords)}")
        print(f"   📖 {c.meaning}")
        if c.yes_no_answer:
            answer_map = {
                "YES": "✅ YES",
                "MAYBE_YES": "🟡 どちらかといえばYES",
                "MAYBE_NO" : "🟠 どちらかといえばNO",
                "NO"       : "❌ NO",
            }
            print(f"   🎯 {answer_map.get(c.yes_no_answer, c.yes_no_answer)}")
    print("\n" + "─" * 52)
    print("  【AIプロンプト用コンテキスト】")
    print(result.to_prompt_context())
    print("═" * 52 + "\n")


if __name__ == "__main__":
    engine = TarotEngine()   # major.json を自動検索

    print("\n▶ ワンオラクル")
    _pretty_print(engine.draw_one(question="今日の運勢は？"))

    print("\n▶ スリーカード")
    _pretty_print(engine.draw_three(question="仕事について知りたい"))

    print("\n▶ YES/NO")
    _pretty_print(engine.draw_yes_no(question="転職すべきか？"))

    print("\n▶ ケルティッククロス（簡易）")
    _pretty_print(engine.draw_celtic_mini(question="恋愛の行方は？"))

    print("\n▶ JSON出力サンプル（ワンオラクル）")
    result = engine.draw_one()
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
