"""
zokan.py — 蔵干算出モジュール（テーブル内蔵版）
"""

ZOKAN_TABLE = {
    "子": ["癸"],
    "丑": ["己", "癸", "辛"],
    "寅": ["甲", "丙", "戊"],
    "卯": ["乙"],
    "辰": ["戊", "乙", "癸"],
    "巳": ["丙", "庚", "戊"],
    "午": ["丁", "己"],
    "未": ["己", "丁", "乙"],
    "申": ["庚", "壬", "戊"],
    "酉": ["辛"],
    "戌": ["戊", "辛", "丁"],
    "亥": ["壬", "甲"],
}

def get_zokan(branch: str) -> list:
    if branch not in ZOKAN_TABLE:
        raise ValueError(f"地支 '{branch}' が zokan テーブルに見つかりません")
    return ZOKAN_TABLE[branch]

def get_zokan_with_ten_gods(branch: str, day_stem: str) -> list:
    from shichu.ten_gods import get_ten_god
    zokan_list = get_zokan(branch)
    result = []
    for stem in zokan_list:
        try:
            god = get_ten_god(day_stem, stem)
        except Exception:
            god = "不明"
        result.append({"stem": stem, "ten_god": god})
    return result

def get_pillar_zokan(day_stem: str, pillars: dict) -> dict:
    result = {}
    for key in ["year", "month", "day", "hour"]:
        if key in pillars and "branch" in pillars[key]:
            branch = pillars[key]["branch"]
            result[f"{key}_zokan"] = get_zokan_with_ten_gods(branch, day_stem)
    return result
