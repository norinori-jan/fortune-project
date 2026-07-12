# fortune_core/shichu/gods.py
from dataclasses import dataclass
from fortune_core.common.stem import Stem
from fortune_core.common.branch import Branch

@dataclass(frozen=True)
class God:
    name: str

class GodsEngine:
    """
    神殺を判定するエンジン
    日干ベース（stem）と日支ベース（branch）の2分類で判定する
    gods.json の構造に完全適合
    """

    def __init__(self, registry_loader):
        self.master = registry_loader.get_gods()

    # ------------------------------------------------------------
    # 日干ベースの神殺（天乙貴人・羊刃・天官貴人・天厨貴人）
    # ------------------------------------------------------------
    def _check_stem_based(self, day_stem: Stem, target_branch: Branch) -> list[God]:
        results = []
        day_name = day_stem.name
        target_name = target_branch.name

        for god_name, data in self.master.items():
            stem_map = data.get("stem")
            if not stem_map:
                continue

            if day_name not in stem_map:
                continue

            allowed = stem_map[day_name]

            # 配列 or 文字列の両方に対応
            if isinstance(allowed, list):
                if target_name in allowed:
                    results.append(God(name=god_name))
            else:
                if target_name == allowed:
                    results.append(God(name=god_name))

        return results

    # ------------------------------------------------------------
    # 日支ベースの神殺（咸池・紅艶・孤辰・寡宿・駅馬・天馬・文昌貴人・学堂・金輿・将星）
    # ------------------------------------------------------------
    def _check_branch_based(self, day_branch: Branch, target_branch: Branch) -> list[God]:
        results = []
        day_branch_name = day_branch.name
        target_name = target_branch.name

        for god_name, data in self.master.items():
            branch_map = data.get("branch")
            if not branch_map:
                continue

            if day_branch_name not in branch_map:
                continue

            expected = branch_map[day_branch_name]

            if target_name == expected:
                results.append(God(name=god_name))

        return results

    # ------------------------------------------------------------
    # 四柱すべての神殺を返す
    # ------------------------------------------------------------
    def determine_gods(self, chart) -> dict[str, list[God]]:
        day_stem = chart.day.stem
        day_branch = chart.day.branch

        targets = {
            "year": chart.year.branch,
            "month": chart.month.branch,
            "day": chart.day.branch,
            "hour": chart.hour.branch,
        }

        results = {k: [] for k in targets.keys()}

        for pos, target_branch in targets.items():
            stem_based = self._check_stem_based(day_stem, target_branch)
            branch_based = self._check_branch_based(day_branch, target_branch)

            results[pos].extend(stem_based)
            results[pos].extend(branch_based)

        return results

