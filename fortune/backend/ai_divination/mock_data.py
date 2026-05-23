"""
モック鑑定文データ

APIキーが設定されていない場合、またはテスト環境で使用する
固定の鑑定文を定義するモジュール

用途:
  - 開発環境でのテスト（API課金発生なし）
  - APIキー未設定時のデモンストレーション
  - ユニットテスト用のスタブデータ
"""

from typing import Dict, Any


class MockDivinationData:
    """
    モック鑑定文データストア
    
    四柱推命と三柱推命の両方のパターンを含む
    """

    # 四柱推命（時柱あり）用の鑑定文
    FOUR_PILLAR_READINGS = [
        {
            "natal_chart": {
                "year_pillar": "甲子",
                "month_pillar": "丙午",
                "day_pillar": "癸卯",
                "hour_pillar": "庚戌"
            },
            "divination": """
【命盤分析】年柱・甲子の積極性と月柱・丙午の行動力が相乗効果を生み出す時期です。日柱・癸卯の柔軟性により、新しい環境への適応が比較的スムーズに進みます。

【今年の運勢】仕事面では責任感の出る年。周囲からの信頼を積み重ねることが、後々の昇進につながる可能性が高い。人間関係は誠実さが評価される時期です。

【具体的なアドバイス】秋から冬にかけて重要な決断が求められる可能性があります。焦らず、周囲の意見を聞きながら判断することが吉。東方面への行動や転換が暗示されています。
""".strip()
        },
        {
            "natal_chart": {
                "year_pillar": "壬申",
                "month_pillar": "甲午",
                "day_pillar": "丁卯",
                "hour_pillar": "乙巳"
            },
            "divination": """
【命盤分析】陰干の相乗により、内省と直感が冴える時期。細かな観察眼が活かされるでしょう。

【今年の運勢】対人関係が重視される1年。信頼構築が次のステップへのカギになります。創造的な仕事での活躍が期待される時期です。

【具体的なアドバイス】北方面への転換が吉。6月から8月は特に注意が必要ですが、適切に対応すれば大きな成長の機会になります。地道な努力が実を結ぶ時期です。
""".strip()
        }
    ]

    # 三柱推命（時柱なし）用の鑑定文
    THREE_PILLAR_READINGS = [
        {
            "natal_chart": {
                "year_pillar": "甲子",
                "month_pillar": "丙午",
                "day_pillar": "癸卯",
                "hour_pillar": None
            },
            "divination": """
【命盤分析】年柱・月柱・日柱の組み合わせから、今期は「変化と適応」がテーマです。時柱が不明のため、より広い視点での解釈となります。

【今年の運勢】全体的には上昇局面。ただし時期ごとに波があるため、柔軟な対応が求められます。人間関係での新しい展開が予想されます。

【具体的なアドバイス】時柱が不明なため、時間帯よりも「月」や「季節」を意識した行動が有効です。春から初夏にかけての判断が1年の方向性を大きく左右します。
""".strip()
        },
        {
            "natal_chart": {
                "year_pillar": "壬申",
                "month_pillar": "甲午",
                "day_pillar": "丁卯",
                "hour_pillar": None
            },
            "divination": """
【命盤分析】三柱推命として解釈すると、「知識と実行」の調和がテーマ。内的な成長と外的な展開が同時進行する時期です。

【今年の運勢】学習や自己啓発に適した1年。新しいスキルの習得や知識の深化が、後々の仕事に直結します。対人関係は質を重視すべき時期。

【具体的なアドバイス】大きな決断は秋以降に。現在は準備と学習の時期と位置づけましょう。南東方面への活動が吉。焦らず着実に進めることが成功のカギです。
""".strip()
        }
    ]

    @classmethod
    def get_mock_divination(
        cls,
        has_hour_pillar: bool = True,
        index: int = 0
    ) -> str:
        """
        モック鑑定文を取得

        Args:
            has_hour_pillar: 時柱があるかどうか（四柱 or 三柱）
            index: 複数パターン中のインデックス

        Returns:
            モック鑑定文
        """
        if has_hour_pillar:
            readings = cls.FOUR_PILLAR_READINGS
        else:
            readings = cls.THREE_PILLAR_READINGS

        # インデックスが範囲外の場合はラップアラウンド
        safe_index = index % len(readings)
        return readings[safe_index]["divination"]

    @classmethod
    def get_all_mock_data(cls) -> Dict[str, Any]:
        """
        すべてのモックデータを取得

        Returns:
            モックデータの完全なセット
        """
        return {
            "four_pillar": cls.FOUR_PILLAR_READINGS,
            "three_pillar": cls.THREE_PILLAR_READINGS
        }

    @classmethod
    def get_demo_response(cls) -> Dict[str, Any]:
        """
        デモンストレーション用のレスポンス例を取得

        Returns:
            API呼び出し不使用時のレスポンス例
        """
        return {
            "divination": cls.get_mock_divination(has_hour_pillar=True, index=0),
            "mode": "mock",
            "note": "APIキーが設定されていないため、モックデータを返しています。本番環境ではAPIキーを設定してください。",
            "model": "mock-claude-3-5-sonnet"
        }
