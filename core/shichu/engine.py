"""
engine.py — 四柱推命コアエンジン
"""

from shichu.registry_loader import get_registry

# 天干・地支リスト
STEMS   = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
BRANCHES = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

# 六十干支（甲子=0）
KANSHI = [
    "甲子","乙丑","丙寅","丁卯","戊辰","己巳","庚午","辛未","壬申","癸酉",
    "甲戌","乙亥","丙子","丁丑","戊寅","己卯","庚辰","辛巳","壬午","癸未",
    "甲申","乙酉","丙戌","丁亥","戊子","己丑","庚寅","辛卯","壬辰","癸巳",
    "甲午","乙未","丙申","丁酉","戊戌","己亥","庚子","辛丑","壬寅","癸卯",
    "甲辰","乙巳","丙午","丁未","戊申","己酉","庚戌","辛亥","壬子","癸丑",
    "甲寅","乙卯","丙辰","丁巳","戊午","己未","庚申","辛酉","壬戌","癸亥",
]

def _kanshi_to_dict(kanshi: str) -> dict:
    stem   = kanshi[0]
    branch = kanshi[1]
    return {"stem": stem, "branch": branch, "kanshi": kanshi}

# ── 年柱 ──────────────────────────────────────────
def get_year_pillar(year: int) -> dict:
    idx = (year - 4) % 60
    return _kanshi_to_dict(KANSHI[idx])

# ── 月柱 ──────────────────────────────────────────
MONTH_BRANCH = ["寅","卯","辰","巳","午","未","申","酉","戌","亥","子","丑"]

MONTH_STEM_BASE = {
    "甲": 0, "己": 0,
    "乙": 2, "庚": 2,
    "丙": 4, "辛": 4,
    "丁": 6, "壬": 6,
    "戊": 8, "癸": 8,
}

def get_month_pillar(year_stem: str, month: int) -> dict:
    branch = MONTH_BRANCH[month - 1]
    base   = MONTH_STEM_BASE[year_stem]
    stem   = STEMS[(base + month - 1) % 10]
    return {"stem": stem, "branch": branch, "kanshi": stem + branch}

# ── 日柱 ──────────────────────────────────────────
def get_day_pillar_from_date(year: int, month: int, day: int) -> dict:
    """ユリウス日から日柱を算出する"""
    if month <= 2:
        year -= 1
        month += 12
    A = year // 100
    B = 2 - A + A // 4
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524
    idx = (jd + 1) % 60
    return _kanshi_to_dict(KANSHI[idx])

# ── 時柱 ──────────────────────────────────────────
HOUR_BRANCH_IDX = [0,0,1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11]

def get_hour_pillar(day_stem: str, hour: int) -> dict:
    branch_idx = HOUR_BRANCH_IDX[hour]
    branch     = BRANCHES[branch_idx]
    base       = MONTH_STEM_BASE[day_stem]
    stem       = STEMS[(base + branch_idx) % 10]
    return {"stem": stem, "branch": branch, "kanshi": stem + branch}

# ── build_meisei ──────────────────────────────────
from shichu.ten_gods import get_pillar_ten_gods
from shichu.twelve_growth import get_pillar_twelve_growths
from shichu.zokan import get_pillar_zokan

def build_meisei(year: int, month: int, day: int, hour: int) -> dict:
    year_pillar  = get_year_pillar(year)
    month_pillar = get_month_pillar(year_pillar["stem"], month)
    day_pillar   = get_day_pillar_from_date(year, month, day)
    hour_pillar  = get_hour_pillar(day_pillar["stem"], hour)

    pillars = {
        "year":  year_pillar,
        "month": month_pillar,
        "day":   day_pillar,
        "hour":  hour_pillar,
    }
    day_stem = day_pillar["stem"]

    return {
        "pillars":        pillars,
        "day_stem":       day_stem,
        "ten_gods":       get_pillar_ten_gods(day_stem, pillars),
        "twelve_growths": get_pillar_twelve_growths(day_stem, pillars),
        "zokan":          get_pillar_zokan(day_stem, pillars),
    }

if __name__ == "__main__":
    import json
    print(json.dumps(build_meisei(1990, 5, 15, 14), ensure_ascii=False, indent=2))
