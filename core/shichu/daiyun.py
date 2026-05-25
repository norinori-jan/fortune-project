"""
daiyun.py — 大運算出モジュール（節入り日精密計算）

大運の流れ:
  - 陽男・陰女 → 生まれた月の次の節気に向かって順行
  - 陰男・陽女 → 生まれた月の前の節気に向かって逆行
  - 節入りまでの日数 ÷ 3 = 大運開始年齢（1日=4ヶ月）
"""

import math
from shichu.engine import (
    get_year_pillar, get_month_pillar, get_day_pillar_from_date,
    get_hour_pillar, STEMS, BRANCHES, KANSHI
)
from shichu.ten_gods import get_ten_god
from shichu.twelve_growth import get_twelve_growth
from shichu.zokan import get_zokan_with_ten_gods

# ── 節気テーブル（月ごとの節入り概算日・時刻補正なし版）
# key: month(1-12), value: (節名, 概算日)
SETSU_APPROX = {
    1:  ("小寒",  6),
    2:  ("立春",  4),
    3:  ("啓蟄",  6),
    4:  ("清明",  5),
    5:  ("立夏",  6),
    6:  ("芒種",  6),
    7:  ("小暑",  7),
    8:  ("立秋",  7),
    9:  ("白露",  8),
    10: ("寒露",  8),
    11: ("立冬",  7),
    12: ("大雪",  7),
}

def _is_yang_stem(stem: str) -> bool:
    """陽干かどうか（甲丙戊庚壬）"""
    return stem in ("甲", "丙", "戊", "庚", "壬")

def _get_setsu_day(year: int, month: int) -> int:
    """指定年月の節入り概算日を返す"""
    return SETSU_APPROX[month][1]

def _days_to_next_setsu(year: int, month: int, day: int) -> int:
    """生まれた日から次の節入りまでの日数（順行用）"""
    setsu_day = _get_setsu_day(year, month)
    if day <= setsu_day:
        return setsu_day - day
    # 次の月の節
    next_month = month % 12 + 1
    next_year  = year + 1 if month == 12 else year
    next_setsu = _get_setsu_day(next_year, next_month)
    # 月の残り日数 + 次月の節入り日
    days_in_month = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        days_in_month[2] = 29
    return (days_in_month[month] - day) + next_setsu

def _days_to_prev_setsu(year: int, month: int, day: int) -> int:
    """生まれた日から前の節入りまでの日数（逆行用）"""
    setsu_day = _get_setsu_day(year, month)
    if day >= setsu_day:
        return day - setsu_day
    # 前の月の節
    prev_month = 12 if month == 1 else month - 1
    prev_year  = year - 1 if month == 1 else year
    prev_setsu = _get_setsu_day(prev_year, prev_month)
    days_in_month = [0,31,28,31,30,31,30,31,31,30,31,30,31]
    if (prev_year % 4 == 0 and prev_year % 100 != 0) or prev_year % 400 == 0:
        days_in_month[2] = 29
    return (days_in_month[prev_month] - prev_setsu) + day

def _next_kanshi(kanshi: str, steps: int = 1) -> str:
    """干支を順行でsteps進める"""
    idx = KANSHI.index(kanshi)
    return KANSHI[(idx + steps) % 60]

def _prev_kanshi(kanshi: str, steps: int = 1) -> str:
    """干支を逆行でsteps戻す"""
    idx = KANSHI.index(kanshi)
    return KANSHI[(idx - steps) % 60]

def _kanshi_to_dict(kanshi: str) -> dict:
    return {"stem": kanshi[0], "branch": kanshi[1], "kanshi": kanshi}

def _build_daiyun_entry(day_stem: str, kanshi: str, start_age: int, period_index: int) -> dict:
    d = _kanshi_to_dict(kanshi)
    return {
        "period":      period_index + 1,
        "start_age":   start_age,
        "end_age":     start_age + 9,
        "kanshi":      kanshi,
        "stem":        d["stem"],
        "branch":      d["branch"],
        "ten_god":     get_ten_god(day_stem, d["stem"]),
        "twelve_growth": get_twelve_growth(day_stem, d["branch"]),
        "zokan":       get_zokan_with_ten_gods(d["branch"], day_stem),
    }

def build_daiyun(year: int, month: int, day: int, gender: str) -> dict:
    """
    大運を算出する。

    Args:
        year, month, day: 生年月日
        gender: "male" or "female"

    Returns:
        {
            "start_age": 3,          # 大運開始年齢
            "direction": "順行",
            "periods": [...]          # 10期分
        }
    """
    year_pillar = get_year_pillar(year)
    month_pillar = get_month_pillar(year_pillar["stem"], month)
    month_kanshi = month_pillar["kanshi"]

    # 陰陽判定
    is_yang_year = _is_yang_stem(year_pillar["stem"])
    is_male = (gender == "male")

    # 順行: 陽年男 or 陰年女
    forward = (is_yang_year and is_male) or (not is_yang_year and not is_male)

    if forward:
        days = _days_to_next_setsu(year, month, day)
    else:
        days = _days_to_prev_setsu(year, month, day)

    # 1日=4ヶ月 → 3日=1年
    start_age = math.ceil(days / 3)

    day_pillar = get_day_pillar_from_date(year, month, day)
    day_stem = day_pillar["stem"]

    # 10期分生成
    periods = []
    for i in range(10):
        if forward:
            k = _next_kanshi(month_kanshi, i + 1)
        else:
            k = _prev_kanshi(month_kanshi, i + 1)
        age = start_age + i * 10
        periods.append(_build_daiyun_entry(day_stem, k, age, i))

    return {
        "start_age": start_age,
        "direction": "順行" if forward else "逆行",
        "periods":   periods,
    }
