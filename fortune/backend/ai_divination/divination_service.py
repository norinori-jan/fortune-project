"""
AI鑑定ビジネスロジック層

機能:
  - APIキーの有無判定
  - モックデータ vs 実API の分岐ロジック
  - エラーハンドリング
  - レスポンス生成

このモジュールにより、Flaskエンドポイントから
実装の詳細（モック/API）を隠蔽できます
"""

import os
from typing import Dict, Any, Optional

try:
    from .mock_data import MockDivinationData
except ImportError:
    from mock_data import MockDivinationData

try:
    from .claude_client import ClaudeAIDivination
except ImportError:
    from claude_client import ClaudeAIDivination


class DivinationService:
    """
    AI鑑定ビジネスロジック層
    
    APIキーの有無に応じて、以下を制御：
    - モックデータの返却
    - 実Claude APIの呼び出し
    """

    def __init__(self):
        """
        DivinationServiceの初期化
        
        - APIキーの有無を検査
        - ClaudeAIDivination インスタンスを条件付きで初期化
        """
        self.has_api_key = self._check_api_key()
        self.claude_client = None

        if self.has_api_key:
            try:
                self.claude_client = ClaudeAIDivination()
            except ValueError as e:
                # APIキーはあるが初期化に失敗した場合
                self.has_api_key = False
                self.error_message = f"Claude API初期化エラー: {str(e)}"

    @staticmethod
    def _check_api_key() -> bool:
        """
        ANTHROPIC_API_KEY が設定されているか確認
        
        Returns:
            APIキーが有効な場合True、未設定の場合False
        """
        api_key = os.getenv("ANTHROPIC_API_KEY")
        return bool(api_key and str(api_key).strip() != "")

    def generate_divination(
        self,
        natal_chart: Dict[str, Any],
        user_query: str,
        use_mock: bool = False
    ) -> Dict[str, Any]:
        """
        鑑定文を生成（モック or 実API）
        
        Args:
            natal_chart: 命盤データ
            user_query: ユーザーの質問
            use_mock: 強制的にモックを使用するフラグ
                     (テスト時に便利)
        
        Returns:
            レスポンス辞書
            {
                "divination": str,         # 鑑定文
                "mode": "mock" or "api",   # 使用モード
                "model": str,              # 使用モデル
                "hour_pillar_mode": "3柱" or "4柱",  # 柱の種類
                "status": "success" or "error",
                "message": str  # ステータスメッセージ
            }
        """
        try:
            # 入力検証
            self._validate_input(natal_chart, user_query)

            # 柱の種類を判定
            hour_pillar_mode = self._detect_pillar_mode(natal_chart)

            # モックを使用するか判定
            if use_mock or not self.has_api_key:
                return self._generate_mock_divination(
                    natal_chart,
                    hour_pillar_mode
                )
            else:
                return self._generate_real_divination(
                    natal_chart,
                    user_query,
                    hour_pillar_mode
                )

        except ValueError as e:
            return {
                "status": "error",
                "error_type": "validation_error",
                "message": str(e),
                "divination": None
            }
        except Exception as e:
            return {
                "status": "error",
                "error_type": "internal_error",
                "message": f"内部エラー: {str(e)}",
                "divination": None
            }

    def _validate_input(
        self,
        natal_chart: Dict[str, Any],
        user_query: str
    ) -> None:
        """
        入力値の検証
        
        Raises:
            ValueError: 入力が不正な場合
        """
        if not isinstance(natal_chart, dict):
            raise ValueError("natal_chart は辞書型である必要があります")

        required_pillars = ["year_pillar", "month_pillar", "day_pillar"]
        for pillar in required_pillars:
            if pillar not in natal_chart:
                raise ValueError(f"natal_chart に {pillar} が含まれていません")

        if not user_query or not isinstance(user_query, str):
            raise ValueError("user_query は空でない文字列である必要があります")

        if len(user_query) > 1000:
            raise ValueError("user_query は1000文字以下である必要があります")

    @staticmethod
    def _detect_pillar_mode(natal_chart: Dict[str, Any]) -> str:
        """
        柱の種類を判定（三柱 or 四柱）
        
        Args:
            natal_chart: 命盤データ
        
        Returns:
            "3柱" or "4柱"
        """
        hour_pillar = natal_chart.get("hour_pillar")
        if hour_pillar and str(hour_pillar).strip():
            return "4柱"
        return "3柱"

    def _generate_mock_divination(
        self,
        natal_chart: Dict[str, Any],
        hour_pillar_mode: str
    ) -> Dict[str, Any]:
        """
        モック鑑定文を生成
        
        Args:
            natal_chart: 命盤データ
            hour_pillar_mode: "3柱" or "4柱"
        
        Returns:
            レスポンス辞書
        """
        has_hour = hour_pillar_mode == "4柱"
        divination_text = MockDivinationData.get_mock_divination(
            has_hour_pillar=has_hour
        )

        return {
            "status": "success",
            "divination": divination_text,
            "mode": "mock",
            "model": "mock-claude-3-5-sonnet",
            "hour_pillar_mode": hour_pillar_mode,
            "message": "APIキーが未設定のため、モックデータを返しています"
        }

    def _generate_real_divination(
        self,
        natal_chart: Dict[str, Any],
        user_query: str,
        hour_pillar_mode: str
    ) -> Dict[str, Any]:
        """
        実Claude APIで鑑定文を生成
        
        Args:
            natal_chart: 命盤データ
            user_query: ユーザーの質問
            hour_pillar_mode: "3柱" or "4柱"
        
        Returns:
            レスポンス辞書
        """
        if not self.claude_client:
            raise RuntimeError("Claude APIクライアントが初期化されていません")

        try:
            divination_text = self.claude_client.generate_divination(
                natal_chart=natal_chart,
                user_query=user_query,
                max_tokens=600
            )

            return {
                "status": "success",
                "divination": divination_text,
                "mode": "api",
                "model": self.claude_client.model,
                "hour_pillar_mode": hour_pillar_mode,
                "message": "Claude APIを使用して鑑定文を生成しました"
            }

        except Exception as e:
            return {
                "status": "error",
                "error_type": "api_error",
                "message": f"Claude API呼び出しエラー: {str(e)}",
                "divination": None
            }

    def get_status(self) -> Dict[str, Any]:
        """
        サービスの状態を取得（デバッグ用）
        
        Returns:
            ステータス情報
        """
        return {
            "has_api_key": self.has_api_key,
            "mode": "api" if self.has_api_key else "mock",
            "message": "Claude API使用可" if self.has_api_key else "モードで動作中"
        }
