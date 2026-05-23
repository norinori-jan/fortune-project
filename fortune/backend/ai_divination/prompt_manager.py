"""
プロンプト管理クラス

機能:
  - システムプロンプトのテンプレート管理
  - 時刻不明（三柱推命）への動的対応
  - 統合環境の文脈を反映したプロンプト生成
  - 命盤データのフォーマット処理

思想: 明朝透派（陽生陰死式・陰陽分離派）
  - データ捏造の禁止
  - 陽生陰死・陰陽分離の遵守
  - 相談者の不安を煽らない
  - 具体的で実践的なアドバイス
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional

# 相対 import のフォールバック対応（直接実行時のサポート）
# このモジュールは他からは相対import されないが、念のため


class PromptManager:
    """
    統合環境における命盤AI鑑定用のプロンプト管理

    文脈:
    - fortune-core: 干支計算・節気判定・大運決定のコアロジック
    - fortune: 四柱推命・奇門遁甲のロジック統合（このモジュール）
    - fenshui_map: 盤面マッピングおよび配置エンジン
    - fengshui-app: UI・エンドポイント

    思想: 明朝透派（陽生陰死式・陰陽分離派）
    """

    def __init__(self, template_dir: Optional[str] = None):
        """
        PromptManagerの初期化

        Args:
            template_dir: システムプロンプトテンプレートのディレクトリパス
                         (デフォルト: このファイルと同じディレクトリ下の 'templates')

        Raises:
            FileNotFoundError: テンプレートファイルが見つからない場合
        """
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"

        self.template_dir = Path(template_dir)
        self.system_prompt_template = self._load_system_prompt()

    def _load_system_prompt(self) -> str:
        """
        システムプロンプトテンプレートを読み込む

        Returns:
            読み込まれたテンプレート文字列

        Raises:
            FileNotFoundError: テンプレートファイルが見つからない場合
        """
        template_path = self.template_dir / "system_prompt.txt"

        if not template_path.exists():
            raise FileNotFoundError(
                f"システムプロンプトテンプレートが見つかりません: {template_path}"
            )

        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()

    def generate_system_prompt(self, natal_chart: Dict[str, Any]) -> str:
        """
        【要件1】システムプロンプトのテンプレート保持

        統合環境の文脈とルールに基づいてシステムプロンプトを生成する

        Args:
            natal_chart: fortune-coreから生成された命盤辞書
                {
                    "year_pillar": "甲子",
                    "month_pillar": "丙寅",
                    "day_pillar": "丁酉",
                    "hour_pillar": "己卯" or None,  ← 時刻不明の場合
                    "ten_stem": {...},
                    "earthly_branch": {...},
                    ...
                }

        Returns:
            生成されたシステムプロンプト文字列
        """
        # テンプレート内の {{...}} プレースホルダーを置換
        system_prompt = self.system_prompt_template

        # 【要件2】時刻不明への動的対応を行う
        has_hour_pillar = self._has_valid_hour_pillar(natal_chart)

        if not has_hour_pillar:
            # 時刻不明（三柱推命）への最適化
            system_prompt = self._apply_three_pillar_mode(system_prompt)
        else:
            # 通常（四柱推命）への最適化
            system_prompt = self._apply_four_pillar_mode(system_prompt)

        return system_prompt

    def _has_valid_hour_pillar(self, natal_chart: Dict[str, Any]) -> bool:
        """
        【要件2】時刻不明判定

        hour_pillar が None または空文字列の場合は False を返す

        Args:
            natal_chart: 命盤データ

        Returns:
            時柱が有効な場合はTrue、不明な場合はFalse
        """
        hour_pillar = natal_chart.get("hour_pillar")
        return hour_pillar is not None and str(hour_pillar).strip() != ""

    def _apply_three_pillar_mode(self, prompt: str) -> str:
        """
        【要件2】時刻不明（三柱推命）用にプロンプトを調整

        - 時柱に関する記述を「時柱：不明（三柱で鑑定）」へ置換
        - AIの解釈を三柱用に最適化

        Args:
            prompt: 元のプロンプト文字列

        Returns:
            調整されたプロンプト文字列
        """
        # プレースホルダー置換
        prompt = prompt.replace(
            "{{HOUR_PILLAR_INFO}}",
            "時柱：不明（時刻が提供されていないため、三柱推命として鑑定を行います）"
        )
        prompt = prompt.replace(
            "{{INTERPRETATION_MODE}}",
            "三柱推命（年柱・月柱・日柱）の組み合わせに基づいて"
        )
        prompt = prompt.replace(
            "{{PILLAR_COUNT}}",
            "3"
        )

        return prompt

    def _apply_four_pillar_mode(self, prompt: str) -> str:
        """
        【要件2】通常の四柱推命用にプロンプトを調整

        Args:
            prompt: 元のプロンプト文字列

        Returns:
            調整されたプロンプト文字列
        """
        prompt = prompt.replace(
            "{{HOUR_PILLAR_INFO}}",
            "時柱を含む完全な四柱推命として鑑定を行います"
        )
        prompt = prompt.replace(
            "{{INTERPRETATION_MODE}}",
            "四柱推命（年柱・月柱・日柱・時柱）の完全な組み合わせに基づいて"
        )
        prompt = prompt.replace(
            "{{PILLAR_COUNT}}",
            "4"
        )

        return prompt

    def generate_user_message(
        self,
        natal_chart: Dict[str, Any],
        user_query: str
    ) -> str:
        """
        ユーザーの質問と命盤データを結合してユーザーメッセージを生成

        Args:
            natal_chart: 命盤データ
            user_query: ユーザーからの質問（例: 「今年の運勢は？」）

        Returns:
            Claude APIへ送信するユーザーメッセージ
        """
        # 命盤データのフォーマット
        chart_info = self._format_natal_chart(natal_chart)

        message = f"""【命盤データ】
{chart_info}

【ご質問】
{user_query}

上記の命盤データに基づいて、ご質問にお答えください。
"""
        return message

    def _format_natal_chart(self, natal_chart: Dict[str, Any]) -> str:
        """
        命盤データを見やすくフォーマット

        Args:
            natal_chart: 命盤データ

        Returns:
            フォーマットされた命盤情報文字列
        """
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

    def get_context_awareness(self) -> str:
        """
        統合環境の文脈を返す（プロンプトテンプレート内に埋め込む用）

        Returns:
            統合環境についての説明文字列
        """
        return """【システム統合環境】
このAI鑑定システムは、以下の4つのモジュールの統合環境で動作しています：

1. **fortune-core**（コアロジック）
   - 干支の計算と検証
   - 節気判定エンジン
   - 大運決定ロジック

2. **fortune**（ロジック統合層）←★このシステムはここに実装
   - 四柱推命解析
   - 奇門遁甲ロジック統合
   - AI鑑定エンジン（本モジュール）

3. **fenshui_map**（空間マッピング層）
   - 盤面マッピングエンジン
   - 方位・配置計算

4. **fengshui-app**（UI・API層）
   - ユーザーインターフェース
   - RESTful APIエンドポイント

【このシステムの役割】
fortune-core で生成された正確な命盤データを受け取り、
明朝透派（陽生陰死式・陰陽分離派）の思想に基づいて、
具体的で実践的な鑑定文を生成します。
"""
