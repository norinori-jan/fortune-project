"""五行・十二支エンジン（風水方位判定 + 紫微斗数の生誕時間推定補助）。"""

from __future__ import annotations

from typing import Dict, Iterable, List, Tuple


ELEMENTS: Tuple[str, ...] = ("木", "火", "土", "金", "水")

# 天干 -> 五行
STEM_TO_ELEMENT: Dict[str, str] = {
    "甲": "木",
    "乙": "木",
    "丙": "火",
    "丁": "火",
    "戊": "土",
    "己": "土",
    "庚": "金",
    "辛": "金",
    "壬": "水",
    "癸": "水",
}

# 地支 -> 本来の五行
BRANCH_TO_ELEMENT: Dict[str, str] = {
    "子": "水",
    "丑": "土",
    "寅": "木",
    "卯": "木",
    "辰": "土",
    "巳": "火",
    "午": "火",
    "未": "土",
    "申": "金",
    "酉": "金",
    "戌": "土",
    "亥": "水",
}

# 1) 二十四山（360度を15度ずつ分割）
# 中心角: 子=0°, 癸=15°, ...（各セクタは中心 ±7.5°）
# 24山の標準配列（羅盤順）
TWENTY_FOUR_MOUNTAINS: List[str] = [
    "子",
    "癸",
    "丑",
    "艮",
    "寅",
    "甲",
    "卯",
    "乙",
    "辰",
    "巽",
    "巳",
    "丙",
    "午",
    "丁",
    "未",
    "坤",
    "申",
    "庚",
    "酉",
    "辛",
    "戌",
    "乾",
    "亥",
    "壬",
]

# 24山記号 -> 五行
MOUNTAIN_TO_ELEMENT: Dict[str, str] = {
    "子": "水",
    "癸": "水",
    "丑": "土",
    "艮": "土",
    "寅": "木",
    "甲": "木",
    "卯": "木",
    "乙": "木",
    "辰": "土",
    "巽": "木",
    "巳": "火",
    "丙": "火",
    "午": "火",
    "丁": "火",
    "未": "土",
    "坤": "土",
    "申": "金",
    "庚": "金",
    "酉": "金",
    "辛": "金",
    "戌": "土",
    "乾": "金",
    "亥": "水",
    "壬": "水",
}

# 要件どおり「辞書」を明示的に提供
TWENTY_FOUR_MOUNTAIN_MAP: Dict[str, Dict[str, float | str | int]] = {}
for idx, mountain in enumerate(TWENTY_FOUR_MOUNTAINS):
    center = idx * 15.0
    start = (center - 7.5) % 360.0
    end = (center + 7.5) % 360.0
    TWENTY_FOUR_MOUNTAIN_MAP[mountain] = {
        "index": idx,
        "center_degree": center,
        "start_degree": start,
        "end_degree": end,
        "element": MOUNTAIN_TO_ELEMENT[mountain],
    }


# 2) 支蔵干と根（強弱付き）
#
# 強弱ウェイト（一般的な「本気/中気/余気」の比重）
ROOT_LEVEL_WEIGHT: Dict[str, float] = {
    "strong": 1.0,  # 本気
    "medium": 0.6,  # 中気
    "weak": 0.3,  # 余気
}

# 各地支に蔵される干（本気/中気/余気）
# 形式: 地支 -> [(干, 強弱), ...]
BRANCH_HIDDEN_STEMS: Dict[str, List[Tuple[str, str]]] = {
    "子": [("癸", "strong")],
    "丑": [("己", "strong"), ("癸", "medium"), ("辛", "weak")],
    "寅": [("甲", "strong"), ("丙", "medium"), ("戊", "weak")],
    "卯": [("乙", "strong")],
    "辰": [("戊", "strong"), ("乙", "medium"), ("癸", "weak")],
    "巳": [("丙", "strong"), ("戊", "medium"), ("庚", "weak")],
    "午": [("丁", "strong"), ("己", "weak")],
    "未": [("己", "strong"), ("丁", "medium"), ("乙", "weak")],
    "申": [("庚", "strong"), ("壬", "medium"), ("戊", "weak")],
    "酉": [("辛", "strong")],
    "戌": [("戊", "strong"), ("辛", "medium"), ("丁", "weak")],
    "亥": [("壬", "strong"), ("甲", "weak")],
}

# 地支 -> 五行の根強度（蔵干を五行へ展開した辞書）
BRANCH_ELEMENT_ROOTS: Dict[str, Dict[str, float]] = {}
for branch, hidden_stems in BRANCH_HIDDEN_STEMS.items():
    element_strength = {element: 0.0 for element in ELEMENTS}
    for stem, level in hidden_stems:
        element = STEM_TO_ELEMENT[stem]
        element_strength[element] += ROOT_LEVEL_WEIGHT[level]
    BRANCH_ELEMENT_ROOTS[branch] = element_strength


class FortuneEngine:
    """風水方位判定 + 五行エネルギー推定を行う統合エンジン。"""

    def get_direction_info(self, degree: float) -> Dict[str, float | str]:
        """
        角度から24山方位と五行を返す。

        Args:
            degree: 任意の角度（負数や360超も可）

        Returns:
            mountain: 24山
            element: 五行
            normalized_degree: 0 <= degree < 360 に正規化した角度
            sector_start/sector_end: 該当セクタ境界
        """
        normalized_degree = degree % 360.0
        index = int((normalized_degree + 7.5) // 15) % 24
        mountain = TWENTY_FOUR_MOUNTAINS[index]
        mountain_info = TWENTY_FOUR_MOUNTAIN_MAP[mountain]
        return {
            "mountain": mountain,
            "element": str(mountain_info["element"]),
            "normalized_degree": normalized_degree,
            "sector_start": float(mountain_info["start_degree"]),
            "sector_end": float(mountain_info["end_degree"]),
        }

    def estimate_element_strength(self, zodiac_list: Iterable[str]) -> Dict[str, float]:
        """
        支リストから五行エネルギー強度を計算する。

        Args:
            zodiac_list: 例 ["寅", "午", "戌"]

        Returns:
            {"木": x, "火": y, "土": z, "金": a, "水": b}
        """
        total_strength = {element: 0.0 for element in ELEMENTS}

        for zodiac in zodiac_list:
            if zodiac not in BRANCH_ELEMENT_ROOTS:
                raise ValueError(f"未対応の地支です: {zodiac}")

            roots = BRANCH_ELEMENT_ROOTS[zodiac]
            for element in ELEMENTS:
                total_strength[element] += roots[element]

        return total_strength


if __name__ == "__main__":
    engine = FortuneEngine()

    # --- 簡易テスト 1: 24山判定 ---
    direction_samples = [0, 7.4, 7.6, 90, 225, 359.9, -10]
    print("=== get_direction_info テスト ===")
    for deg in direction_samples:
        info = engine.get_direction_info(deg)
        print(f"{deg:6}° -> {info['mountain']} ({info['element']})")

    # --- 簡易テスト 2: 五行強度推定 ---
    # 火局（寅午戌）を例に、火と木・土が相対的に乗ることを確認
    sample_zodiacs = ["寅", "午", "戌"]
    result = engine.estimate_element_strength(sample_zodiacs)

    print("\n=== estimate_element_strength テスト ===")
    print(f"入力支: {sample_zodiacs}")
    print("五行強度:", result)

    # 最低限のアサーション
    assert engine.get_direction_info(0)["mountain"] == "子"
    assert engine.get_direction_info(90)["mountain"] == "卯"
    assert result["火"] > result["金"]
    assert sum(result.values()) > 0

    print("\n簡易テスト完了: OK")