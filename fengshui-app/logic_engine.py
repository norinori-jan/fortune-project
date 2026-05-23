from __future__ import annotations

from typing import Dict, List


PALACE_ORDER: List[str] = ["坎", "艮", "震", "巽", "離", "坤", "兌", "乾"]
PALACE_CENTER_DEGREE: Dict[str, float] = {
    "坎": 0.0,
    "艮": 45.0,
    "震": 90.0,
    "巽": 135.0,
    "離": 180.0,
    "坤": 225.0,
    "兌": 270.0,
    "乾": 315.0,
}
PALACE_TO_COMPASS: Dict[str, str] = {
    "坎": "北",
    "艮": "北東",
    "震": "東",
    "巽": "南東",
    "離": "南",
    "坤": "南西",
    "兌": "西",
    "乾": "北西",
}

# 八宅: 宅卦 -> 方位配置
HOUSE_GUA_MAP: Dict[str, Dict[str, str]] = {
    "坎": {
        "伏位": "坎",
        "生気": "巽",
        "天医": "震",
        "延年": "離",
        "絶命": "坤",
        "五鬼": "乾",
        "六煞": "兌",
        "禍害": "艮",
    },
    "艮": {
        "伏位": "艮",
        "生気": "坤",
        "天医": "乾",
        "延年": "兌",
        "絶命": "巽",
        "五鬼": "震",
        "六煞": "離",
        "禍害": "坎",
    },
    "震": {
        "伏位": "震",
        "生気": "離",
        "天医": "坎",
        "延年": "巽",
        "絶命": "兌",
        "五鬼": "艮",
        "六煞": "坤",
        "禍害": "乾",
    },
    "巽": {
        "伏位": "巽",
        "生気": "坎",
        "天医": "離",
        "延年": "震",
        "絶命": "艮",
        "五鬼": "坤",
        "六煞": "乾",
        "禍害": "兌",
    },
    "離": {
        "伏位": "離",
        "生気": "震",
        "天医": "巽",
        "延年": "坎",
        "絶命": "乾",
        "五鬼": "兌",
        "六煞": "艮",
        "禍害": "坤",
    },
    "坤": {
        "伏位": "坤",
        "生気": "艮",
        "天医": "兌",
        "延年": "乾",
        "絶命": "坎",
        "五鬼": "巽",
        "六煞": "震",
        "禍害": "離",
    },
    "兌": {
        "伏位": "兌",
        "生気": "乾",
        "天医": "坤",
        "延年": "艮",
        "絶命": "震",
        "五鬼": "離",
        "六煞": "坎",
        "禍害": "巽",
    },
    "乾": {
        "伏位": "乾",
        "生気": "兌",
        "天医": "艮",
        "延年": "坤",
        "絶命": "離",
        "五鬼": "坎",
        "六煞": "巽",
        "禍害": "震",
    },
}


def normalize_degree(degree: float) -> float:
    return degree % 360.0


def get_seat_degree(facing_degree: float) -> float:
    return normalize_degree(facing_degree + 180.0)


def get_palace_by_degree(degree: float) -> str:
    normalized = normalize_degree(degree)
    index = int((normalized + 22.5) // 45) % 8
    return PALACE_ORDER[index]


def _format_position(palace: str) -> Dict[str, float | str]:
    return {
        "palace": palace,
        "direction": PALACE_TO_COMPASS[palace],
        "center_degree": PALACE_CENTER_DEGREE[palace],
    }


def get_house_gua_info(facing_degree: float) -> Dict[str, object]:
    facing = normalize_degree(facing_degree)
    seat = get_seat_degree(facing)
    seat_palace = get_palace_by_degree(seat)

    house_map = HOUSE_GUA_MAP[seat_palace]
    lucky_map = {
        key: _format_position(house_map[key])
        for key in ("生気", "天医", "延年", "伏位")
    }
    unlucky_map = {
        key: _format_position(house_map[key])
        for key in ("絶命", "五鬼", "六煞", "禍害")
    }

    return {
        "facing_degree": facing,
        "seat_degree": seat,
        "seat_palace": seat_palace,
        "house_name": f"{seat_palace}宅",
        "lucky_directions": lucky_map,
        "unlucky_directions": unlucky_map,
    }
