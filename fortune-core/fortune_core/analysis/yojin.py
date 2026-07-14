# fortune_core/analysis/yojin.py

from dataclasses import dataclass

from .element_strength import ElementStrength
from .kakukyoku import KakukyokuResult


@dataclass(frozen=True)
class YojinResult:
    """
    用神判定結果
    """
    yojin: str | None
    kishin: str | None
    kishin2: str | None
    kyoshin: str | None


class YojinAnalyzer:
    """
    用神・喜神・忌神判定
    """

    def analyze(
        self,
        day_element: str,
        strength: ElementStrength,
        kakukyoku: KakukyokuResult,
    ) -> YojinResult:

        values = strength.values

        self_value = values.get(day_element, 0)

        # --------------------------------------------------
        # 従格
        # --------------------------------------------------
        if kakukyoku.jugaku:

            return self._jugaku(day_element, kakukyoku.jugaku)

        # --------------------------------------------------
        # 身弱
        # --------------------------------------------------
        if self_value < 2.5:

            return self._weak(day_element)

        # --------------------------------------------------
        # 身旺
        # --------------------------------------------------
        return self._strong(day_element)

    # --------------------------------------------------
    # 身弱
    # --------------------------------------------------
    def _weak(self, element):

        table = {
            "木": ("水", "木", "金", "土"),
            "火": ("木", "火", "水", "金"),
            "土": ("火", "土", "木", "水"),
            "金": ("土", "金", "火", "木"),
            "水": ("金", "水", "土", "火"),
        }

        y, k1, k2, x = table[element]

        return YojinResult(
            yojin=y,
            kishin=k1,
            kishin2=k2,
            kyoshin=x,
        )

    # --------------------------------------------------
    # 身旺
    # --------------------------------------------------
    def _strong(self, element):

        table = {
            "木": ("金", "土", "火", "水"),
            "火": ("水", "金", "土", "木"),
            "土": ("木", "水", "金", "火"),
            "金": ("火", "木", "水", "土"),
            "水": ("土", "火", "木", "金"),
        }

        y, k1, k2, x = table[element]

        return YojinResult(
            yojin=y,
            kishin=k1,
            kishin2=k2,
            kyoshin=x,
        )

    # --------------------------------------------------
    # 従格
    # --------------------------------------------------
    def _jugaku(self, element, jugaku):

        table = {
            "従旺格": ("比劫", "印綬", None, "官殺"),
            "従財格": ("財", "食傷", None, "比劫"),
            "従殺格": ("官殺", "財", None, "印綬"),
            "従児格": ("食傷", "財", None, "印綬"),
        }

        y, k1, k2, x = table.get(
            jugaku,
            (None, None, None, None)
        )

        return YojinResult(
            yojin=y,
            kishin=k1,
            kishin2=k2,
            kyoshin=x,
        )