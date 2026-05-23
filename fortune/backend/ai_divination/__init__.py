"""
AI鑑定エンジン（Claude API統合）

統合環境構成:
  fortune-core: 干支計算・節気判定・大運決定のコアロジック
  fortune: 四柱推命・奇門遁甲のロジック統合 ← このモジュール
  fenshui_map: 盤面マッピングおよび配置エンジン
  fengshui-app: UI・エンドポイント

思想: 明朝透派（陽生陰死式・陰陽分離派）

このモジュールは、fortune-coreから生成された命盤データをClaude APIに渡し、
明朝透派思想に基づいた鑑定文を生成するための機能を提供します。

機能:
  - システムプロンプトのテンプレート管理
  - 時刻不明（三柱推命）への動的対応
  - Claude APIとの統合
"""

from .prompt_manager import PromptManager
from .claude_client import ClaudeAIDivination

__all__ = ["PromptManager", "ClaudeAIDivination"]
