"""
engine_patch.py
--------------
既存の engine.py に追加するコードの差分です。
engine.py の末尾にこのコードをコピーしてください。

追加する関数:
  - build_meisei(year, month, day, hour) → 命式フル JSON
"""

# ===== engine.py の末尾に追加 =====

from shichu.ten_gods import get_pillar_ten_gods
from shichu.twelve_growth import get_pillar_twelve_growths
from shichu.zokan import get_pillar_zokan


def build_meisei(year: int, month: int, day: int, hour: int) -> dict:
    """
    生年月日時から命式（四柱＋十神＋十二運＋蔵干）を算出する。

    Args:
        year:  西暦年（例: 1990）
        month: 月（1〜12）
        day:   日（1〜31）
        hour:  時（0〜23）

    Returns:
        {
            "pillars": {
                "year":  {"stem": "庚", "branch": "午", "kanshi": "庚午"},
                "month": {"stem": "甲", "branch": "子", "kanshi": "甲子"},
                "day":   {"stem": "丙", "branch": "申", "kanshi": "丙申"},
                "hour":  {"stem": "庚", "branch": "子", "kanshi": "庚子"},
            },
            "day_stem": "丙",
            "ten_gods": {
                "year_stem_god":  "偏財",
                "month_stem_god": "偏印",
                "day_stem_god":   "比肩",
                "hour_stem_god":  "偏財",
            },
            "twelve_growths": {
                "year_branch_growth":  "長生",
                "month_branch_growth": "胎",
                "day_branch_growth":   "絶",
                "hour_branch_growth":  "胎",
            },
            "zokan": {
                "year_zokan":  [{"stem": "己", "ten_god": "傷官"}, {"stem": "丁", "ten_god": "比肩"}],
                "month_zokan": [{"stem": "癸", "ten_god": "正官"}],
                "day_zokan":   [{"stem": "庚", "ten_god": "偏財"}, {"stem": "壬", "ten_god": "偏官"}, {"stem": "戊", "ten_god": "食神"}],
                "hour_zokan":  [{"stem": "癸", "ten_god": "正官"}],
            }
        }
    """
    # 四柱算出（既存関数を呼ぶ）
    year_pillar  = get_year_pillar(year)
    month_pillar = get_month_pillar(year_pillar["stem"], month)
    day_pillar   = get_day_pillar_from_date(year, month, day)   # ← 要確認: 既存関数名に合わせる
    hour_pillar  = get_hour_pillar(day_pillar["stem"], hour)

    pillars = {
        "year":  year_pillar,
        "month": month_pillar,
        "day":   day_pillar,
        "hour":  hour_pillar,
    }

    day_stem = day_pillar["stem"]

    # 十神・十二運・蔵干
    ten_gods       = get_pillar_ten_gods(day_stem, pillars)
    twelve_growths = get_pillar_twelve_growths(day_stem, pillars)
    zokan          = get_pillar_zokan(day_stem, pillars)

    return {
        "pillars":        pillars,
        "day_stem":       day_stem,
        "ten_gods":       ten_gods,
        "twelve_growths": twelve_growths,
        "zokan":          zokan,
    }


# ===== 動作確認用スニペット（engine.py と同じ場所で実行）=====
if __name__ == "__main__":
    import json
    result = build_meisei(1990, 5, 15, 14)
    print(json.dumps(result, ensure_ascii=False, indent=2))
