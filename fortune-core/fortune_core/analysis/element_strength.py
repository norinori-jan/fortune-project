# fortune_core/analysis/element_strength.py

from dataclasses import dataclass

from fortune_core.shichu.relation import RelationEngine


# ------------------------------------------------------------
# 判定結果
# ------------------------------------------------------------

@dataclass(frozen=True)
class ElementStrengthResult:
    """
    五行量計算結果
    """

    values: dict[str, float]
    hogo: str | None
    kaikyoku: str | None

    @property
    def total(self) -> float:
        return sum(self.values.values())

    @property
    def strongest(self) -> str:
        return max(self.values, key=self.values.get)

    @property
    def weakest(self) -> str:
        return min(self.values, key=self.values.get)


# ------------------------------------------------------------
# 五行量解析
# ------------------------------------------------------------

class ElementStrengthAnalyzer:

    """
    五行量を集計する

    対象

        ・天干
        ・地支
        ・蔵干
        ・方合
        ・会局（三合）
    """

    STEM_WEIGHT = 1.0
    BRANCH_WEIGHT = 1.0
    ZANGKAN_WEIGHT = 0.5

    def __init__(self):

        self.relation = RelationEngine()

    # ------------------------------------------------------------
    # メイン
    # ------------------------------------------------------------

    def analyze(self, chart):

        values = {
            "木": 0.0,
            "火": 0.0,
            "土": 0.0,
            "金": 0.0,
            "水": 0.0,
        }

        ##########################################################
        # 方合・会局判定
        ##########################################################

        branches = [
            chart.year.branch,
            chart.month.branch,
            chart.day.branch,
            chart.hour.branch,
        ]

        hogo = self.relation.find_hogo(branches)
        kaikyoku = self.relation.find_kaikyoku(branches)

        change_element = None
        converted = set()

        if hogo is not None:
            change_element = hogo.element
            converted = {b.name for b in hogo.branches}

        elif kaikyoku is not None:
            change_element = kaikyoku.element
            converted = {b.name for b in kaikyoku.branches}

        ##########################################################
        # 天干
        ##########################################################

        for pillar in (
            chart.year,
            chart.month,
            chart.day,
            chart.hour,
        ):
            values[pillar.stem.element] += self.STEM_WEIGHT

        ##########################################################
        # 地支＋蔵干
        ##########################################################

        for pillar in (
            chart.year,
            chart.month,
            chart.day,
            chart.hour,
        ):

            branch = pillar.branch

            ##########################################
            # 方合・会局
            ##########################################

            if (
                change_element is not None
                and branch.name in converted
            ):

                values[change_element] += self.BRANCH_WEIGHT
                values[change_element] += self.ZANGKAN_WEIGHT

                continue

            ##########################################
            # 通常地支
            ##########################################

            values[branch.element] += self.BRANCH_WEIGHT

            ##########################################
            # 蔵干
            ##########################################

            if pillar.zangkan is not None:

                values[
                    pillar.zangkan.element
                ] += self.ZANGKAN_WEIGHT

        ##########################################################
        # 結果
        ##########################################################

        return ElementStrengthResult(
            values=values,
            hogo=hogo.element if hogo else None,
            kaikyoku=kaikyoku.element if kaikyoku else None,
        )