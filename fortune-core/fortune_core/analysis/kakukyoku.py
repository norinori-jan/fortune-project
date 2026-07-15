# fortune_core/analysis/kakukyoku.py

from dataclasses import dataclass

from fortune_core.analysis.element_strength import (
    ElementStrengthResult,
)


@dataclass(frozen=True)
class KakukyokuResult:
    """
    格局判定結果
    """

    kakukyoku: str
    body_strength: str
    jugaku: str | None


class KakukyokuAnalyzer:
    """
    格局判定エンジン
    """

    def analyze(
        self,
        chart,
        strength: ElementStrengthResult,
    ) -> KakukyokuResult:

        values = strength.values

        day_element = chart.day.stem.element

        body_strength = self._body_strength(
            day_element,
            values,
        )

        kakukyoku = self._normal_kakukyoku(chart)

        jugaku = self._detect_jugaku(
            day_element,
            values,
        )

        if jugaku is not None:
            kakukyoku = jugaku

        return KakukyokuResult(
            kakukyoku=kakukyoku,
            body_strength=body_strength,
            jugaku=jugaku,
        )

    # ----------------------------------------------------
    # 身旺・身弱
    # ----------------------------------------------------

    def _body_strength(
        self,
        day_element,
        values,
    ):

        mine = values[day_element]

        if mine >= 3.5:
            return "身旺"

        if mine >= 2.0:
            return "中和"

        return "身弱"

    # ----------------------------------------------------
    # 通常格局
    # ----------------------------------------------------

    def _normal_kakukyoku(self, chart):

        month_branch = chart.month.branch.name

        mapping = {
            "寅": "建禄格",
            "卯": "建禄格",
            "巳": "食神格",
            "午": "傷官格",
            "申": "偏官格",
            "酉": "正官格",
            "亥": "偏印格",
            "子": "印綬格",
        }

        return mapping.get(
            month_branch,
            "普通格"
        )

    # ----------------------------------------------------
    # 従格
    # ----------------------------------------------------

    def _detect_jugaku(
        self,
        day_element,
        values,
    ):

        mine = values[day_element]

        if mine > 0.5:
            return None

        if day_element == "木":

            if values["火"] >= 2.5:
                return "従財格"

            if values["金"] >= 2.5:
                return "従殺格"

        if day_element == "水":

            if values["木"] >= 2.5:
                return "従児格"

        if mine == 0:
            return "従旺格"

        return None