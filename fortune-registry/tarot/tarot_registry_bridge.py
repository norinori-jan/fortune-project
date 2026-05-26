"""
tarot_registry_bridge.py
========================
fortune-core の FORTUNE_REGISTRY / registry_a.json と
TarotEngine を繋ぐブリッジモジュール。

- draw して結果を FORTUNE_REGISTRY 形式の dict に変換
- Google Sheets (Apps Script) 向け JSON を生成
- iPhone Safari Web App の IndexedDB 向けペイロードを生成
"""

import json
from datetime import datetime
from tarot_engine import TarotEngine, SpreadType, SpreadResult


# ────────────────────────────────────────────
#  registry_a.json 形式へのブリッジ
# ────────────────────────────────────────────

class TarotRegistryBridge:
    """
    FORTUNE_REGISTRY アーキテクチャとの統合クラス。

    registry_a.json の "tarot" セクションに追記できる形式と、
    Google Apps Script 経由で Sheets に書き込める行データを生成する。
    """

    def __init__(self, json_path: str = "major.json"):
        self.engine = TarotEngine(json_path)

    # ── 占い実行 + エントリ生成 ─────────────

    def execute_and_export(
        self,
        spread_type: SpreadType = SpreadType.ONE_ORACLE,
        question: str | None = None,
    ) -> dict:
        """
        占いを実行し、FORTUNE_REGISTRY エントリを返す。

        Returns
        -------
        dict  registry_a.json["tarot"] に appendできる形式
        """
        result = self.engine.draw(spread_type, question=question)
        return self._to_registry_entry(result)

    # ── 変換メソッド ──────────────────────

    def _to_registry_entry(self, result: SpreadResult) -> dict:
        """SpreadResult → FORTUNE_REGISTRY エントリ"""
        return {
            # --- メタ ---
            "type"         : "tarot_reading",
            "schema_ver"   : "1.0.0",
            "spread"       : result.spread_type.value,
            "spread_label" : result.spread_label,
            "drawn_at"     : result.drawn_at,
            "question"     : result.question,

            # --- カード一覧 ---
            "cards"        : [c.to_dict() for c in result.cards],

            # --- AI プロンプト用コンテキスト ---
            "prompt_context": result.to_prompt_context(),

            # --- Google Sheets 向け単純化行データ ---
            "sheets_row"   : self._to_sheets_row(result),

            # --- IndexedDB (Safari Web App) 向けペイロード ---
            "idb_payload"  : self._to_idb_payload(result),
        }

    @staticmethod
    def _to_sheets_row(result: SpreadResult) -> dict:
        """
        Google Apps Script で Sheets に書き込む際の
        1行フラット形式（列名 → 値）。

        Apps Script 側:
            sheet.appendRow(Object.values(payload.sheets_row));
        """
        row = {
            "drawn_at"    : result.drawn_at,
            "spread"      : result.spread_label,
            "question"    : result.question or "",
        }
        for c in result.cards:
            prefix = c.position_label
            row[f"{prefix}_card"]        = c.name_ja
            row[f"{prefix}_orientation"] = "正位置" if c.orientation.value == "upright" else "逆位置"
            row[f"{prefix}_keywords"]    = "・".join(c.keywords)
        return row

    @staticmethod
    def _to_idb_payload(result: SpreadResult) -> dict:
        """
        iPhone Safari Web App の IndexedDB に格納するペイロード。
        キー: `tarot_${drawn_at}` を推奨。
        """
        return {
            "key"     : f"tarot_{result.drawn_at.replace(':', '-')}",
            "spread"  : result.spread_type.value,
            "question": result.question,
            "cards"   : [
                {
                    "pos"  : c.position_label,
                    "id"   : c.card_id,
                    "name" : c.name_ja,
                    "ori"  : c.orientation.value,
                    "kw"   : c.keywords,
                }
                for c in result.cards
            ],
            "saved_at": result.drawn_at,
        }


# ────────────────────────────────────────────
#  AI 読み取りプロンプトビルダー
# ────────────────────────────────────────────

SYSTEM_PROMPT_TEMPLATE = """\
あなたは神秘的で洞察力のあるタロット占い師「叡智の声」です。
以下のルールで占いの解読を行ってください。

- 日本語で、詩的かつ親しみやすい文体で語りかけてください
- 各カードの意味を統合し、全体的なメッセージとして伝えてください
- 「{spread_label}」の文脈（{positions}）を必ず考慮してください
- 300〜500文字程度でまとめてください
- 最後に一言、励ましや行動のヒントを添えてください
"""

def build_ai_prompt(result: SpreadResult) -> tuple[str, str]:
    """
    Claude API に渡す (system_prompt, user_message) を生成する。

    使い方:
        system, user = build_ai_prompt(result)
        # → Claude API に送信
    """
    positions = "・".join(
        SPREAD_POSITIONS_LABEL.get(result.spread_type, [c.position_label for c in result.cards])
    )
    system = SYSTEM_PROMPT_TEMPLATE.format(
        spread_label=result.spread_label,
        positions=positions,
    )
    user = result.to_prompt_context()
    return system, user


SPREAD_POSITIONS_LABEL = {
    SpreadType.ONE_ORACLE : ["現在の状況"],
    SpreadType.THREE_CARD : ["過去", "現在", "未来"],
    SpreadType.CELTIC_MINI: ["現在の状況", "課題", "顕在意識", "潜在意識", "結果"],
    SpreadType.YES_NO     : ["答え"],
    SpreadType.DAILY      : ["今日のメッセージ"],
}


# ────────────────────────────────────────────
#  CLI デモ
# ────────────────────────────────────────────

if __name__ == "__main__":
    bridge = TarotRegistryBridge("major.json")

    print("\n== FORTUNE_REGISTRY エントリ（スリーカード）==")
    entry = bridge.execute_and_export(
        spread_type=SpreadType.THREE_CARD,
        question="今の自分に必要なものは何か？",
    )
    print(json.dumps(entry, ensure_ascii=False, indent=2))

    print("\n== AI プロンプトプレビュー ==")
    result = bridge.engine.draw_one(question="今日の一歩は？")
    system, user = build_ai_prompt(result)
    print("--- SYSTEM ---")
    print(system)
    print("--- USER ---")
    print(user)
