# fortune_core/shichu/gods.py

from dataclasses import dataclass

from fortune_core.common.stem import Stem
from fortune_core.common.branch import Branch


@dataclass(frozen=True)
class God:
    """神殺"""
    name: str


class GodsEngine:
    """
    神殺判定エンジン

    gods.json

    {
        "天乙貴人":{
            "stem":{...}
        },
        "駅馬":{
            "branch":{...}
        }
    }

    に対応する。
    """

    def __init__(self, registry_loader):
        self.master = registry_loader.get_gods()

    # ---------------------------------------------------------
    # 日干基準
    # ---------------------------------------------------------
    def _check_stem_based(
        self,
        day_stem: Stem,
        target_branch: Branch,
    ) -> list[God]:

        result = []

        for god_name, data in self.master.items():

            stem_table = data.get("stem")
            if stem_table is None:
                continue

            branches = stem_table.get(day_stem.name)
            if branches is None:
                continue

            if isinstance(branches, str):
                branches = [branches]

            if target_branch.name in branches:
                result.append(God(god_name))

        return result

    # ---------------------------------------------------------
    # 日支基準
    # ---------------------------------------------------------
    def _check_branch_based(
        self,
        day_branch: Branch,
        target_branch: Branch,
    ) -> list[God]:

        result = []

        for god_name, data in self.master.items():

            branch_table = data.get("branch")
            if branch_table is None:
                continue

            branches = branch_table.get(day_branch.name)
            if branches is None:
                continue

            if isinstance(branches, str):
                branches = [branches]

            if target_branch.name in branches:
                result.append(God(god_name))

        return result

    # ---------------------------------------------------------
    # 四柱判定
    # ---------------------------------------------------------
    def determine_gods(self, chart):

        day_stem = chart.day.stem
        day_branch = chart.day.branch

        pillars = {
            "year": chart.year.branch,
            "month": chart.month.branch,
            "day": chart.day.branch,
            "hour": chart.hour.branch,
        }

        result = {}

        for pillar_name, branch in pillars.items():

            gods = []

            gods.extend(
                self._check_stem_based(
                    day_stem,
                    branch,
                )
            )

            gods.extend(
                self._check_branch_based(
                    day_branch,
                    branch,
                )
            )

            result[pillar_name] = gods

        return result