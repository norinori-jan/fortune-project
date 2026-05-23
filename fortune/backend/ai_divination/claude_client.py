"""
Claude API実行クラス

機能:
  - Anthropic SDK との連携
  - API呼び出しとエラーハンドリング
  - 命盤データとユーザー質問の統合処理

要件: APIキーは os.getenv("ANTHROPIC_API_KEY") から安全に取得
"""

import os
from typing import Dict, Any, Optional

from anthropic import Anthropic

try:
    from .prompt_manager import PromptManager
except ImportError:
    from prompt_manager import PromptManager


class ClaudeAIDivination:
    """
    【要件3】Claude APIとの統合

    命盤データとユーザー質問をClaude APIに渡し、
    明朝透派思想に基づいた鑑定文を生成する

    使用例:
        >>> divination = ClaudeAIDivination()
        >>> natal_chart = {
        ...     "year_pillar": "甲子",
        ...     "month_pillar": "丙寅",
        ...     "day_pillar": "丁酉",
        ...     "hour_pillar": "己卯"
        ... }
        >>> result = divination.generate_divination(
        ...     natal_chart=natal_chart,
        ...     user_query="今年の運勢は？"
        ... )
        >>> print(result)
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        prompt_manager: Optional[PromptManager] = None,
        model: str = "claude-3-5-sonnet-20241022"
    ):
        """
        ClaudeAIDivinationの初期化

        Args:
            api_key: Anthropic APIキー
                    (省略時は環境変数 ANTHROPIC_API_KEY から取得)
            prompt_manager: PromptManager インスタンス
                           (省略時は新規作成)
            model: 使用するClaude モデル
                  (デフォルト: claude-3-5-sonnet-20241022)

        Raises:
            ValueError: APIキーが設定されていない場合
        """
        if api_key is None:
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError(
                    "ANTHROPIC_API_KEY が設定されていません。"
                    "環境変数またはコンストラクタ引数で指定してください。"
                )

        self.client = Anthropic(api_key=api_key)
        self.prompt_manager = prompt_manager or PromptManager()
        self.model = model

    def generate_divination(
        self,
        natal_chart: Dict[str, Any],
        user_query: str,
        max_tokens: int = 1000
    ) -> str:
        """
        命盤鑑定文を生成

        Args:
            natal_chart: fortune-core から生成された命盤データ
                {
                    "year_pillar": str,
                    "month_pillar": str,
                    "day_pillar": str,
                    "hour_pillar": str or None,  ← 時刻不明時はNone
                    ...
                }
            user_query: ユーザーの質問
                       (例: "今年の運勢は？", "どのような適職がありますか？")
            max_tokens: 生成する最大トークン数
                       (目安: 300文字なら500程度)

        Returns:
            生成された鑑定文（300文字程度）

        Raises:
            ValueError: 入力データが不正な場合
            RuntimeError: Claude API呼び出しエラー
        """
        # 入力検証
        if not isinstance(natal_chart, dict):
            raise ValueError("natal_chart は辞書型である必要があります")

        if not user_query or not isinstance(user_query, str):
            raise ValueError("user_query は空でない文字列である必要があります")

        try:
            # システムプロンプト生成（【要件1】【要件2】）
            system_prompt = self.prompt_manager.generate_system_prompt(
                natal_chart
            )

            # ユーザーメッセージ生成
            user_message = self.prompt_manager.generate_user_message(
                natal_chart,
                user_query
            )

            # Claude API呼び出し（【要件3】）
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": user_message
                    }
                ]
            )

            # レスポンス抽出
            divination_text = response.content[0].text

            return divination_text

        except Exception as e:
            raise RuntimeError(
                f"Claude API呼び出しエラー: {str(e)}"
            ) from e

    def generate_divination_with_context(
        self,
        natal_chart: Dict[str, Any],
        user_query: str,
        additional_context: Optional[str] = None,
        max_tokens: int = 1000
    ) -> str:
        """
        追加コンテキストを含めた鑑定文生成

        相談者の特殊な状況や懸念事項などを加味した鑑定を行う場合に使用

        Args:
            natal_chart: 命盤データ
            user_query: ユーザーの質問
            additional_context: 追加情報
                               (例: 相談者の状況、懸念事項、職業など)
            max_tokens: 最大トークン数

        Returns:
            生成された鑑定文

        Raises:
            ValueError: 入力データが不正な場合
            RuntimeError: Claude API呼び出しエラー
        """
        # ユーザーメッセージに追加コンテキストを含める
        if additional_context:
            extended_query = f"{user_query}\n\n【追加情報】\n{additional_context}"
        else:
            extended_query = user_query

        return self.generate_divination(
            natal_chart,
            extended_query,
            max_tokens
        )

    def get_model_info(self) -> Dict[str, str]:
        """
        使用しているClaudeモデルの情報を返す

        Returns:
            モデル情報
        """
        return {
            "model": self.model,
            "api_provider": "Anthropic"
        }
