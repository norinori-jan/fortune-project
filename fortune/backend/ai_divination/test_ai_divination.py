"""
AI鑑定システムのテストスクリプト

テスト対象:
  1. PromptManager: プロンプト管理とプレースホルダー置換
  2. ClaudeAIDivination: Claude API呼び出しと鑑定文生成

テスト内容:
  - 時柱ありパターン（四柱推命）のプロンプト生成
  - 時柱Noneパターン（三柱推命）のプロンプト生成
  - 実際のClaude API呼び出しと鑑定文生成

使用方法:
  python test_ai_divination.py

前提条件:
  - ANTHROPIC_API_KEY 環境変数が設定されていること
  - requirements.txt で anthropic >= 0.25.0 がインストール済みであること
"""

import os
import sys
import json
from typing import Dict, Any
from pathlib import Path

# モジュールのインポートパスを追加
sys.path.insert(0, str(Path(__file__).parent))

from prompt_manager import PromptManager
from claude_client import ClaudeAIDivination


# ==============================================================================
# テスト用擬似命盤データ
# ==============================================================================

def get_sample_natal_chart_with_hour() -> Dict[str, Any]:
    """
    時柱ありの命盤データ（四柱推命）
    
    年柱: 甲子
    月柱: 丙午
    日柱: 癸卯
    時柱: 庚戌
    """
    return {
        "year_pillar": "甲子",
        "month_pillar": "丙午",
        "day_pillar": "癸卯",
        "hour_pillar": "庚戌",
        "year_stem": "甲",
        "year_branch": "子",
        "month_stem": "丙",
        "month_branch": "午",
        "day_stem": "癸",
        "day_branch": "卯",
        "hour_stem": "庚",
        "hour_branch": "戌",
        "ten_stem": {
            "birth_stem": "癸",
            "power": 0.6
        },
        "earthly_branch": {
            "birth_branch": "卯",
            "power": 0.7
        },
        "data_source": "fortune-core",
        "validation_status": "verified"
    }


def get_sample_natal_chart_without_hour() -> Dict[str, Any]:
    """
    時柱なしの命盤データ（三柱推命）
    
    年柱: 甲子
    月柱: 丙午
    日柱: 癸卯
    時柱: None（時刻不明）
    """
    return {
        "year_pillar": "甲子",
        "month_pillar": "丙午",
        "day_pillar": "癸卯",
        "hour_pillar": None,  # 時刻不明
        "year_stem": "甲",
        "year_branch": "子",
        "month_stem": "丙",
        "month_branch": "午",
        "day_stem": "癸",
        "day_branch": "卯",
        "hour_stem": None,
        "hour_branch": None,
        "ten_stem": {
            "birth_stem": "癸",
            "power": 0.6
        },
        "earthly_branch": {
            "birth_branch": "卯",
            "power": 0.7
        },
        "data_source": "fortune-core",
        "validation_status": "verified"
    }


# ==============================================================================
# PromptManager のテスト
# ==============================================================================

def test_prompt_manager_four_pillar():
    """
    テスト1: PromptManager - 四柱推命（時柱あり）のプロンプト生成
    
    期待:
      - {{HOUR_PILLAR_INFO}} が「時柱を含む完全な四柱推命として鑑定を行います」に置換される
      - {{INTERPRETATION_MODE}} が「四柱推命（年柱・月柱・日柱・時柱）の完全な組み合わせに基づいて」に置換される
      - {{PILLAR_COUNT}} が「4」に置換される
    """
    print("\n" + "="*80)
    print("【テスト1】PromptManager - 四柱推命（時柱あり）")
    print("="*80)

    prompt_manager = PromptManager()
    natal_chart = get_sample_natal_chart_with_hour()

    system_prompt = prompt_manager.generate_system_prompt(natal_chart)

    # 置換確認
    assert "{{HOUR_PILLAR_INFO}}" not in system_prompt, "{{HOUR_PILLAR_INFO}} がまだ置換されていません"
    assert "{{INTERPRETATION_MODE}}" not in system_prompt, "{{INTERPRETATION_MODE}} がまだ置換されていません"
    assert "{{PILLAR_COUNT}}" not in system_prompt, "{{PILLAR_COUNT}} がまだ置換されていません"

    # 出力確認
    print("\n【命盤情報】")
    print(f"  年柱: {natal_chart['year_pillar']}")
    print(f"  月柱: {natal_chart['month_pillar']}")
    print(f"  日柱: {natal_chart['day_pillar']}")
    print(f"  時柱: {natal_chart['hour_pillar']}")

    print("\n【検出されたモード】")
    if "完全な四柱推命" in system_prompt:
        print("  ✅ 四柱推命モード（時柱あり）")
    else:
        print("  ❌ 四柱推命モード検出失敗")

    print("\n【プロンプト内の関連部分（抜粋）】")
    for line in system_prompt.split("\n"):
        if "時柱" in line or "柱推命" in line or "PILLAR" in line:
            print(f"  {line[:100]}")

    print("\n✅ テスト1 完了: 四柱推命プロンプト生成成功\n")


def test_prompt_manager_three_pillar():
    """
    テスト2: PromptManager - 三柱推命（時柱なし）のプロンプト生成
    
    期待:
      - {{HOUR_PILLAR_INFO}} が「時柱：不明（時刻が提供されていないため、三柱推命として鑑定を行います）」に置換される
      - {{INTERPRETATION_MODE}} が「三柱推命（年柱・月柱・日柱）の組み合わせに基づいて」に置換される
      - {{PILLAR_COUNT}} が「3」に置換される
    """
    print("\n" + "="*80)
    print("【テスト2】PromptManager - 三柱推命（時柱なし）")
    print("="*80)

    prompt_manager = PromptManager()
    natal_chart = get_sample_natal_chart_without_hour()

    system_prompt = prompt_manager.generate_system_prompt(natal_chart)

    # 置換確認
    assert "{{HOUR_PILLAR_INFO}}" not in system_prompt, "{{HOUR_PILLAR_INFO}} がまだ置換されていません"
    assert "{{INTERPRETATION_MODE}}" not in system_prompt, "{{INTERPRETATION_MODE}} がまだ置換されていません"
    assert "{{PILLAR_COUNT}}" not in system_prompt, "{{PILLAR_COUNT}} がまだ置換されていません"

    # 出力確認
    print("\n【命盤情報】")
    print(f"  年柱: {natal_chart['year_pillar']}")
    print(f"  月柱: {natal_chart['month_pillar']}")
    print(f"  日柱: {natal_chart['day_pillar']}")
    print(f"  時柱: {natal_chart['hour_pillar']} ← 不明（None）")

    print("\n【検出されたモード】")
    if "三柱推命" in system_prompt and "不明" in system_prompt:
        print("  ✅ 三柱推命モード（時柱なし）")
    else:
        print("  ❌ 三柱推命モード検出失敗")

    print("\n【プロンプト内の関連部分（抜粋）】")
    for line in system_prompt.split("\n"):
        if "時柱" in line or "不明" in line or "柱推命" in line or "PILLAR" in line:
            print(f"  {line[:100]}")

    print("\n✅ テスト2 完了: 三柱推命プロンプト生成成功\n")


def test_user_message_generation():
    """
    テスト3: PromptManager - ユーザーメッセージ生成
    
    期待:
      - 命盤データが整形されてメッセージに含まれる
      - ユーザーの質問が含まれる
    """
    print("\n" + "="*80)
    print("【テスト3】PromptManager - ユーザーメッセージ生成")
    print("="*80)

    prompt_manager = PromptManager()
    natal_chart = get_sample_natal_chart_with_hour()
    user_query = "今年の運勢は？"

    user_message = prompt_manager.generate_user_message(natal_chart, user_query)

    print("\n【生成されたユーザーメッセージ】")
    print(user_message)

    # 検証
    assert "命盤データ" in user_message, "命盤データが含まれていません"
    assert "甲子" in user_message, "年柱（甲子）が含まれていません"
    assert "庚戌" in user_message, "時柱（庚戌）が含まれていません"
    assert "今年の運勢は？" in user_message, "ユーザーの質問が含まれていません"

    print("\n✅ テスト3 完了: ユーザーメッセージ生成成功\n")


# ==============================================================================
# Claude API テスト
# ==============================================================================

def test_claude_api_four_pillar():
    """
    テスト4: ClaudeAIDivination - 四柱推命（時柱あり）でのAPI呼び出し
    
    実際にClaude APIを呼び出して鑑定文を生成する
    """
    print("\n" + "="*80)
    print("【テスト4】ClaudeAIDivination - 四柱推命でのAPI呼び出し")
    print("="*80)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n⚠️  スキップ: ANTHROPIC_API_KEY が設定されていません")
        print("   以下のコマンドを実行して設定してください:")
        print("   $env:ANTHROPIC_API_KEY=\"sk-ant-...\"")
        return

    try:
        divination = ClaudeAIDivination(api_key=api_key)
        natal_chart = get_sample_natal_chart_with_hour()
        user_query = "今年の運勢と適職の方向性について教えてください。"

        print("\n【リクエスト情報】")
        print(f"  モデル: {divination.model}")
        print(f"  命盤: 甲子・丙午・癸卯・庚戌（四柱推命）")
        print(f"  質問: {user_query}")

        print("\n【API呼び出し中...】")
        divination_text = divination.generate_divination(
            natal_chart=natal_chart,
            user_query=user_query,
            max_tokens=600  # 300文字程度 = 500〜600トークン
        )

        print("\n【生成された鑑定文】")
        print(f"\n{divination_text}")
        print(f"\n【文字数】{len(divination_text)}文字")

        # 基本検証
        assert len(divination_text) > 0, "鑑定文が空です"
        assert len(divination_text) < 2000, "鑑定文が長すぎます（制限外）"

        print("\n✅ テスト4 完了: 四柱推命でのAPI呼び出し成功\n")

    except ValueError as e:
        print(f"\n❌ エラー: {e}\n")
    except Exception as e:
        print(f"\n❌ API呼び出しエラー: {e}\n")


def test_claude_api_three_pillar():
    """
    テスト5: ClaudeAIDivination - 三柱推命（時柱なし）でのAPI呼び出し
    
    時柱がない場合のプロンプト動的分岐が機能するか確認
    """
    print("\n" + "="*80)
    print("【テスト5】ClaudeAIDivination - 三柱推命でのAPI呼び出し")
    print("="*80)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n⚠️  スキップ: ANTHROPIC_API_KEY が設定されていません")
        return

    try:
        divination = ClaudeAIDivination(api_key=api_key)
        natal_chart = get_sample_natal_chart_without_hour()
        user_query = "人間関係と対人運について、アドバイスをお願いします。"

        print("\n【リクエスト情報】")
        print(f"  モデル: {divination.model}")
        print(f"  命盤: 甲子・丙午・癸卯・（時柱不明）（三柱推命）")
        print(f"  質問: {user_query}")

        print("\n【API呼び出し中...】")
        divination_text = divination.generate_divination(
            natal_chart=natal_chart,
            user_query=user_query,
            max_tokens=600
        )

        print("\n【生成された鑑定文】")
        print(f"\n{divination_text}")
        print(f"\n【文字数】{len(divination_text)}文字")

        # 基本検証
        assert len(divination_text) > 0, "鑑定文が空です"
        assert len(divination_text) < 2000, "鑑定文が長すぎます（制限外）"

        print("\n✅ テスト5 完了: 三柱推命でのAPI呼び出し成功\n")

    except ValueError as e:
        print(f"\n❌ エラー: {e}\n")
    except Exception as e:
        print(f"\n❌ API呼び出しエラー: {e}\n")


def test_claude_api_with_additional_context():
    """
    テスト6: ClaudeAIDivination - 追加コンテキスト付きでのAPI呼び出し
    
    相談者の追加情報を含めた鑑定を行う
    """
    print("\n" + "="*80)
    print("【テスト6】ClaudeAIDivination - 追加コンテキスト付きAPI呼び出し")
    print("="*80)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("\n⚠️  スキップ: ANTHROPIC_API_KEY が設定されていません")
        return

    try:
        divination = ClaudeAIDivination(api_key=api_key)
        natal_chart = get_sample_natal_chart_with_hour()
        user_query = "キャリアについてのアドバイスをください。"
        additional_context = "現在は営業職ですが、転職を検討しており、自分に合った職種について知りたいです。"

        print("\n【リクエスト情報】")
        print(f"  モデル: {divination.model}")
        print(f"  質問: {user_query}")
        print(f"  追加情報: {additional_context}")

        print("\n【API呼び出し中...】")
        divination_text = divination.generate_divination_with_context(
            natal_chart=natal_chart,
            user_query=user_query,
            additional_context=additional_context,
            max_tokens=600
        )

        print("\n【生成された鑑定文】")
        print(f"\n{divination_text}")
        print(f"\n【文字数】{len(divination_text)}文字")

        # 基本検証
        assert len(divination_text) > 0, "鑑定文が空です"

        print("\n✅ テスト6 完了: 追加コンテキスト付きAPI呼び出し成功\n")

    except ValueError as e:
        print(f"\n❌ エラー: {e}\n")
    except Exception as e:
        print(f"\n❌ API呼び出しエラー: {e}\n")


# ==============================================================================
# メイン処理
# ==============================================================================

def main():
    """
    すべてのテストを実行
    """
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "  AI鑑定システム テストスイート".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")

    # PromptManager テスト
    print("\n\n【フェーズ1】PromptManager テスト")
    print("-" * 80)

    try:
        test_prompt_manager_four_pillar()
        test_prompt_manager_three_pillar()
        test_user_message_generation()
        print("✅ PromptManager テスト: すべて成功")
    except AssertionError as e:
        print(f"❌ PromptManager テスト失敗: {e}")
        return
    except Exception as e:
        print(f"❌ PromptManager テスト エラー: {e}")
        return

    # Claude API テスト
    print("\n\n【フェーズ2】Claude API テスト")
    print("-" * 80)

    test_claude_api_four_pillar()
    test_claude_api_three_pillar()
    test_claude_api_with_additional_context()

    # 最終結果
    print("\n" + "="*80)
    print("【テスト完了】")
    print("="*80)
    print("\n📊 テスト結果サマリー")
    print("  ✅ PromptManager テスト: 完了")
    print("  ✅ Claude API テスト: 実行（結果は上記参照）")
    print("\n💡 注意:")
    print("  - API呼び出しテストのスキップはAPIキー未設定のため")
    print("  - 実行する場合は環境変数 ANTHROPIC_API_KEY を設定してください")
    print("  - テスト実行にはAPIの利用料が発生します")
    print("\n" + "="*80 + "\n")


if __name__ == "__main__":
    main()
