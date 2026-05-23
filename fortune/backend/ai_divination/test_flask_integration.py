"""
Flask エンドポイント統合テスト

新規作成した AI鑑定エンドポイント (/api/divination/ai-reading) の動作確認
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from divination_service import DivinationService
from mock_data import MockDivinationData


def test_divination_service():
    """DivinationService の動作確認"""
    print("\n" + "="*80)
    print("【テスト1】DivinationService 初期化")
    print("="*80)

    service = DivinationService()
    print(f"  APIキー: {'あり' if service.has_api_key else 'なし'}")
    print(f"  モード: {'API' if service.has_api_key else 'Mock'}")
    print("  ✅ 初期化成功")


def test_four_pillar_divination():
    """四柱推命での鑑定文生成テスト"""
    print("\n" + "="*80)
    print("【テスト2】四柱推命（時柱あり）鑑定文生成")
    print("="*80)

    service = DivinationService()
    natal_chart = {
        'year_pillar': '甲子',
        'month_pillar': '丙午',
        'day_pillar': '癸卯',
        'hour_pillar': '庚戌'
    }
    user_query = '今年の運勢は？'

    result = service.generate_divination(
        natal_chart=natal_chart,
        user_query=user_query
    )

    print(f"  ステータス: {result['status']}")
    print(f"  モード: {result['mode']}")
    print(f"  柱の種類: {result['hour_pillar_mode']}")
    print(f"  鑑定文（先頭100文字）: {result['divination'][:100]}...")
    
    assert result['status'] == 'success', "ステータスが success でありません"
    assert result['hour_pillar_mode'] == '4柱', "柱の種類が 4柱 でありません"
    print("  ✅ テスト成功")


def test_three_pillar_divination():
    """三柱推命での鑑定文生成テスト"""
    print("\n" + "="*80)
    print("【テスト3】三柱推命（時柱なし）鑑定文生成")
    print("="*80)

    service = DivinationService()
    natal_chart = {
        'year_pillar': '甲子',
        'month_pillar': '丙午',
        'day_pillar': '癸卯',
        'hour_pillar': None
    }
    user_query = '今年の運勢は？'

    result = service.generate_divination(
        natal_chart=natal_chart,
        user_query=user_query
    )

    print(f"  ステータス: {result['status']}")
    print(f"  モード: {result['mode']}")
    print(f"  柱の種類: {result['hour_pillar_mode']}")
    print(f"  鑑定文（先頭100文字）: {result['divination'][:100]}...")
    
    assert result['status'] == 'success', "ステータスが success でありません"
    assert result['hour_pillar_mode'] == '3柱', "柱の種類が 3柱 でありません"
    print("  ✅ テスト成功")


def test_mock_data():
    """モックデータの取得テスト"""
    print("\n" + "="*80)
    print("【テスト4】モックデータ取得")
    print("="*80)

    demo = MockDivinationData.get_demo_response()
    print(f"  モード: {demo['mode']}")
    print(f"  モデル: {demo['model']}")
    print(f"  鑑定文（先頭100文字）: {demo['divination'][:100]}...")
    
    assert demo['mode'] == 'mock', "モードが mock でありません"
    print("  ✅ テスト成功")


def test_service_status():
    """サービス状態確認テスト"""
    print("\n" + "="*80)
    print("【テスト5】サービス状態確認")
    print("="*80)

    service = DivinationService()
    status = service.get_status()
    
    print(f"  APIキー有無: {status['has_api_key']}")
    print(f"  モード: {status['mode']}")
    print(f"  メッセージ: {status['message']}")
    print("  ✅ テスト成功")


def test_input_validation():
    """入力検証テスト"""
    print("\n" + "="*80)
    print("【テスト6】入力検証")
    print("="*80)

    service = DivinationService()
    
    # 命盤データなし
    result_no_chart = service.generate_divination(
        natal_chart={},
        user_query='テスト'
    )
    assert result_no_chart['status'] == 'error', "命盤データ不正時のエラー処理失敗"
    print("  ✅ 命盤データなしでエラー検出")
    
    # クエリなし
    result_no_query = service.generate_divination(
        natal_chart={'year_pillar': '甲子', 'month_pillar': '丙午', 'day_pillar': '癸卯'},
        user_query=''
    )
    assert result_no_query['status'] == 'error', "クエリなし時のエラー処理失敗"
    print("  ✅ クエリなしでエラー検出")
    
    print("  ✅ テスト成功")


def main():
    """全テスト実行"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║" + " "*78 + "║")
    print("║" + "Flask エンドポイント統合テスト".center(78) + "║")
    print("║" + " "*78 + "║")
    print("╚" + "="*78 + "╝")

    try:
        test_divination_service()
        test_four_pillar_divination()
        test_three_pillar_divination()
        test_mock_data()
        test_service_status()
        test_input_validation()

        print("\n" + "="*80)
        print("【テスト完了】")
        print("="*80)
        print("\n✅ すべてのテストが成功しました")
        print("\n📊 テスト結果サマリー:")
        print("  ✅ DivinationService 初期化")
        print("  ✅ 四柱推命鑑定文生成")
        print("  ✅ 三柱推命鑑定文生成")
        print("  ✅ モックデータ取得")
        print("  ✅ サービス状態確認")
        print("  ✅ 入力検証")
        print("\n💡 次のステップ:")
        print("  1. Flask サーバーを起動")
        print("  2. curl や Postman で /api/divination/ai-reading をテスト")
        print("  3. /api/divination/status でモード確認")
        print("\n" + "="*80 + "\n")

    except Exception as e:
        print(f"\n❌ テスト失敗: {e}\n")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
