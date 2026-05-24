from pathlib import Path
from fortune.backend.ai_divination.prompt_loader import load_prompt

"""
プロンプト管理クラス

機能:
  - システムプロンプトのテンプレート管理（SSOT: fortune-registry/prompts/*.json）
  - 時刻不明（三柱推命）への動的対応
  - 統合環境の文脈を反映したプロンプト生成
  - 命盤データのフォーマット処理

思想: 明朝透派（陽生陰死式・陰陽分離派）
"""

from typing import Dict, Any


class PromptManager:
    """
    統合環境における命盤AI鑑定用のプロンプト管理
    """

    def __init__(self, prompt_name: str = "shichu"):
        """
        prompt_name: 使用するプロンプト名（shichu / meihua / tarot など）
        """
        self.prompt_name = prompt_name

        # SSOT（fortune-registry/prompts/*.json）から読み込む
        prompt_json = load_prompt(prompt_name)

        # JSON の "system" フィールドをテンプレートとして使う
        self.system_prompt_template = prompt_json.get("system", "")

    # ─────────────────────────────────────────────
    # システムプロンプト生成
    # ─────────────────────────────────────────────

    def generate_system_prompt(self, natal_chart: Dict[str, Any]) -> str:
        """
        統合環境の文脈とルールに基づいてシステムプロンプトを生成する
        """
        system_prompt = self.system_prompt_template

        # 時刻不明（三柱推命）かどうか
        has_hour_pillar = self._has_valid_hour_pillar(natal_chart)

        if not has_hour_pillar:
            system_prompt = self._apply_three_pillar_mode(system_prompt)
        else:
            system_prompt = self._apply_four_pillar_mode(system_prompt)

        return system_prompt

    # ─────────────────────────────────────────────
    # 三柱 / 四柱 切り替え
    # ─────────────────────────────────────────────

    def _has_valid_hour_pillar(self, natal_chart: Dict[str, Any]) -> bool:
        hour_pillar = natal_chart.get("hour_pillar")
        return hour_pillar is not None and str(hour_pillar).strip() != ""

    def _apply_three_pillar_mode(self, prompt: str) -> str:
        prompt = prompt.replace(
            "{{HOUR_PILLAR_INFO}}",
            "時柱：不明（時刻が提供されていないため、三柱推命として鑑定を行います）"
        )
        prompt = prompt.replace(
            "{{INTERPRETATION_MODE}}",
            "三柱推命（年柱・月柱・日柱）の組み合わせに基づいて"
        )
        prompt = prompt.replace("{{PILLAR_COUNT}}", "3")
        return prompt

    def _apply_four_pillar_mode(self, prompt: str) -> str:
        prompt = prompt.replace(
            "{{HOUR_PILLAR_INFO}}",
            "時柱を含む完全な四柱推命として鑑定を行います"
        )
        prompt = prompt.replace(
            "{{INTERPRETATION_MODE}}",
            "四柱推命（年柱・月柱・日柱・時柱）の完全な組み合わせに基づいて"
        )
        prompt = prompt.replace("{{PILLAR_COUNT}}", "4")
        return prompt

    # ─────────────────────────────────────────────
    # ユーザーメッセージ生成
    # ─────────────────────────────────────────────

    def generate_user_message(self, natal_chart: Dict[str, Any], user_query: str) -> str:
        chart_info = self._format_natal_chart(natal_chart)

        message = f"""【命盤データ】
{chart_info}

【ご質問】
{user_query}

上記の命盤データに基づいて、ご質問にお答えください。
"""
        return message

    # ─────────────────────────────────────────────
    # 命盤フォーマット
    # ─────────────────────────────────────────────

    def _format_natal_chart(self, natal_chart: Dict[str, Any]) -> str:
        formatted = []
        formatted.append(f"年柱: {natal_chart.get('year_pillar', 'N/A')}")
        formatted.append(f"月柱: {natal_chart.get('month_pillar', 'N/A')}")
        formatted.append(f"日柱: {natal_chart.get('day_pillar', 'N/A')}")

        hour_pillar = natal_chart.get('hour_pillar')
        if hour_pillar and str(hour_pillar).strip():
            formatted.append(f"時柱: {hour_pillar}")
        else:
            formatted.append("時柱: 不明（時刻未提供）")

        return "\n".join(formatted)

    # ─────────────────────────────────────────────
    # 統合環境の説明
    # ─────────────────────────────────────────────

    def get_context_awareness(self) -> str:
        return """【システム統合環境】
このAI鑑定システムは、以下の4つのモジュールの統合環境で動作しています：

1. fortune-core（コアロジック）
2. fortune（四柱推命・奇門遁甲ロジック統合）
3. fenshui_map（盤面マッピング）
4. fengshui-app（UI・API）

fortune-core で生成された正確な命盤データを受け取り、
明朝透派の思想に基づいて、具体的で実践的な鑑定文を生成します。
"""
