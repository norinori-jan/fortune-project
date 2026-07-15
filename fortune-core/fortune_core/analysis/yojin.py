# fortune_core/analysis/yojin.py

from dataclasses import dataclass

from fortune_core.analysis.element_strength import (
    ElementStrengthResult,
)

from fortune_core.analysis.kakukyoku import (
    KakukyokuResult,
)


@dataclass(frozen=True)
class YojinResult:
    """
    用神判定結果
    """

    yojin: str
    kishin: str
    kishin_element: str
    imigami: str


class YojinAnalyzer:
    """
    用神・喜神・忌神判定
    """

    # ------------------------------------------------------------
    # メイン
    # ------------------------------------------------------------

    def analyze(
        self,
        chart,
        strength: ElementStrengthResult,
        kakukyoku: KakukyokuResult,
    ) -> YojinResult:

        day_element = chart.day.stem.element

        body = kakukyoku.body_strength

        if kakukyoku.jugaku:
            return self._jugaku(
                day_element,
                kakukyoku.jugaku,
            )

        if body == "身旺":
            return self._strong(day_element)

        if body == "身弱":
            return self._weak(day_element)

        return self._balanced(day_element)

    # ------------------------------------------------------------
    # 身旺
    # ------------------------------------------------------------

    def _strong(self, elem):

        table = {

            "木": ("金", "土", "木"),
            "火": ("水", "金", "火"),
            "土": ("木", "水", "土"),
            "金": ("火", "土", "金"),
            "水": ("土", "火", "水"),

        }

        yojin, kishin, imi = table[elem]

        return YojinResult(
            yojin=yojin,
            kishin=kishin,
            kishin_element=kishin,
            imigami=imi,
        )

    # ------------------------------------------------------------
    # 身弱
    # ------------------------------------------------------------

    def _weak(self, elem):

        table = {

            "木": ("水", "木", "金"),
            "火": ("木", "火", "水"),
            "土": ("火", "土", "木"),
            "金": ("土", "金", "火"),
            "水": ("金", "水", "土"),

        }

        yojin, kishin, imi = table[elem]

        return YojinResult(
            yojin=yojin,
            kishin=kishin,
            kishin_element=kishin,
            imigami=imi,
        )

    # ------------------------------------------------------------
    # 中和
    # ------------------------------------------------------------

    def _balanced(self, elem):

        return YojinResult(
            yojin=elem,
            kishin=elem,
            kishin_element=elem,
            imigami="なし",
        )

    # ------------------------------------------------------------
    # 従格
    # ------------------------------------------------------------

    def _jugaku(
        self,
        elem,
        jugaku,
    ):

        table = {

            "従旺格": ("比劫", "印綬", "官殺"),

            "従財格": ("財", "食傷", "印"),

            "従殺格": ("官殺", "財", "印"),

            "従児格": ("食傷", "財", "印"),

        }

        yojin, kishin, imi = table.get(
            jugaku,
            ("中和", "中和", "なし"),
        )

        return YojinResult(
            yojin=yojin,
            kishin=kishin,
            kishin_element=kishin,
            imigami=imi,
        )