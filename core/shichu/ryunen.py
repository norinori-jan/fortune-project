"""
ryunen.py — 流年算出モジュール

指定した年範囲の流年（年干支＋十神＋十二運＋蔵干）を返す。
"""

from shichu.engine import get_year_pillar, KANSHI
from shichu.ten_gods import get_ten_god
from shichu.twelve_growth import get_twelve_growth
from shichu.zokan import get_zokan_with_ten_gods

def build_ryunen(day_stem: str, start_year: int, end_year: int) -> list:
    """
    流年リストを返す。

    Args:
        day_stem:   日干（例: "壬"）
        start_year: 開始年（西暦）
        end_year:   終了年（西暦）

    Returns:
        [
            {
                "year":         2024,
                "kanshi":       "甲辰",
                "stem":         "甲",
                "branch":       "辰",
                "ten_god":      "食神",
                "twelve_growth":"衰",
                "zokan":        [...],
            },
            ...
        ]
    """
    result = []
    for year in range(start_year, end_year + 1):
        pillar = get_year_pillar(year)
        stem   = pillar["stem"]
        branch = pillar["branch"]
        result.append({
            "year":          year,
            "kanshi":        pillar["kanshi"],
            "stem":          stem,
            "branch":        branch,
            "ten_god":       get_ten_god(day_stem, stem),
            "twelve_growth": get_twelve_growth(day_stem, branch),
            "zokan":         get_zokan_with_ten_gods(branch, day_stem),
        })
    return result
