# fortune_core/shichu/twelve_growth.py
from dataclasses import dataclass
from fortune_core.common.stem import Stem
from fortune_core.common.branch import Branch

@dataclass(frozen=True)
class TwelveGrowth:
    """十二運の情報を保持するデータクラス"""
    name: str   # 長生、沐浴、冠帯、建禄、帝旺、衰、病、死、墓、絶、胎、養
    score: int  # エネルギーの力量（1〜12）

class TwelveGrowthEngine:
    def __init__(self, registry_loader):
        """
        registry_loader から twelve_growth.json の定義データを取得する
        """
        self.master = registry_loader.get_twelve_growth()

    def get_growth(self, day_stem: Stem, branch: Branch) -> TwelveGrowth:
        """
        日主の五行 × 地支 → 十二運を返す
        """
        day_element = day_stem.five_elements  # 木・火・土・金・水
        branch_name = branch.name             # 子・丑・寅…

        if day_element not in self.master:
            raise ValueError(f"無効な五行です: {day_element}")

        element_table = self.master[day_element]

        if branch_name not in element_table:
            raise ValueError(f"無効な地支です: {branch_name}")

        data = element_table[branch_name]

        return TwelveGrowth(name=data["name"], score=data["score"])

    def evaluate(self, chart):
        """
        Chart から四柱それぞれの十二運を返す
        """
        day_stem = chart.day.stem

        return {
            "year": self.get_growth(day_stem, chart.year.branch),
            "month": self.get_growth(day_stem, chart.month.branch),
            "day": self.get_growth(day_stem, chart.day.branch),
            "hour": self.get_growth(day_stem, chart.hour.branch)
        }


