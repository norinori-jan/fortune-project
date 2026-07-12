# fortune_core/shichu/ten_gods.py
from dataclasses import dataclass
from fortune_core.common.stem import Stem

@dataclass(frozen=True)
class TenGod:
    """通変星の情報を保持するデータクラス"""
    name: str  # 比肩、劫財など
    code: str  # hikata, gozai など（プログラム処理やUI用）

@dataclass(frozen=True)
class TenGodsResult:
    """四柱それぞれの十神"""
    year: TenGod
    month: TenGod
    day: TenGod
    hour: TenGod


class TenGodsEngine:
    def __init__(self, registry_loader):
        self.ten_gods_master = registry_loader.get_ten_gods()
        self.element_map = {"木": 0, "火": 1, "土": 2, "金": 3, "水": 4}

    def _determine_relation(self, day_element: str, target_element: str) -> str:
        day_idx = self.element_map[day_element]
        target_idx = self.element_map[target_element]
        diff = (target_idx - day_idx) % 5

        if diff == 0:
            return "比和"
        elif diff == 1:
            return "我生"
        elif diff == 2:
            return "我克"
        elif diff == 3:
            return "克我"
        elif diff == 4:
            return "生我"

        raise ValueError("五行の判定に失敗しました")

    def get_ten_god(self, day_stem: Stem, target_stem: Stem) -> TenGod:
        relation = self._determine_relation(day_stem.five_elements, target_stem.five_elements)
        yin_yang_relation = "同性" if day_stem.yin_yang == target_stem.yin_yang else "異性"
        god_data = self.ten_gods_master[relation][yin_yang_relation]
        return TenGod(name=god_data["name"], code=god_data["code"])

    def evaluate(self, chart) -> TenGodsResult:
        day_stem = chart.day.stem

        return TenGodsResult(
            year=self.get_ten_god(day_stem, chart.year.stem),
            month=self.get_ten_god(day_stem, chart.month.stem),
            day=TenGod(name="比肩", code="hikata"),  # 日主自身は比肩
            hour=self.get_ten_god(day_stem, chart.hour.stem)
        )

