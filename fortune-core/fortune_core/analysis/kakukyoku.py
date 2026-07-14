# fortune_core/analysis/kakukyoku.py

from dataclasses import dataclass

from fortune_core.shichu.dataclasses import Chart
from .element_strength import ElementStrength


@dataclass(frozen=True)
class KakukyokuResult:
    """
    格局判定結果
    """
    kakukyoku: str | None
    jugaku: str | None


class KakukyokuAnalyzer:
    """
    格局・従格判定
    """

    def analyze(
        self,
        chart: Chart,
        strength: ElementStrength,
    ) -> KakukyokuResult:

        values = strength.values
        day_element = chart.day.stem.element

        jugaku = self._detect_jugaku(day_element, values)
        kakukyoku = self._detect_kakukyoku(chart)

        return KakukyokuResult(
            kakukyoku=kakukyoku,
            jugaku=jugaku,
        )

    # ------------------------------------------------------------
    # 従格判定
    # ------------------------------------------------------------
    def _detect_jugaku(
        self,
        day_element: str,
        values: dict[str, float],
    ) -> str | None:

        if values.get(day_element, 0) > 0.5:
            return None

        if day_element == "木":

            if values["火"] >= 2.5:
                return "従児格"

            if values["土"] >= 2.5:
                return "従財格"

            if values["金"] >= 2.5:
                return "従殺格"

        elif day_element == "火":

            if values["土"] >= 2.5:
                return "従児格"

            if values["金"] >= 2.5:
                return "従財格"

            if values["水"] >= 2.5:
                return "従殺格"

        elif day_element == "土":

            if values["金"] >= 2.5:
                return "従児格"

            if values["水"] >= 2.5:
                return "従財格"

            if values["木"] >= 2.5:
                return "従殺格"

        elif day_element == "金":

            if values["水"] >= 2.5:
                return "従児格"

            if values["木"] >= 2.5:
                return "従財格"

            if values["火"] >= 2.5:
                return "従殺格"

        elif day_element == "水":

            if values["木"] >= 2.5:
                return "従児格"

            if values["火"] >= 2.5:
                return "従財格"

            if values["土"] >= 2.5:
                return "従殺格"

        return None

    # ------------------------------------------------------------
    # 一般格局（仮実装）
    # ------------------------------------------------------------
    def _detect_kakukyoku(
        self,
        chart: Chart,
    ) -> str | None:

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

        return mapping.get(month_branch)