# fortune_core/report/paper.py

from dataclasses import dataclass

from fortune_core.analysis.element_strength import ElementStrength
from fortune_core.analysis.kakukyoku import KakukyokuResult
from fortune_core.analysis.yojin import YojinResult
from fortune_core.analysis.combinations import CombinationResult
from fortune_core.analysis.house_gods import HouseGodResult
from fortune_core.analysis.ai_reading import AIReading


@dataclass(frozen=True)
class PaperReport:
    """
    鑑定書データ

    HTML・PDF・API が共通利用する
    """

    chart: object

    element_strength: ElementStrength

    kakukyoku: KakukyokuResult | None

    yojin: YojinResult | None

    combinations: CombinationResult | None

    house_gods: HouseGodResult | None

    ai_reading: AIReading | None


class PaperBuilder:
    """
    鑑定書生成

    Engineで作成した命式と
    analysis層の解析結果を
    1つのオブジェクトへまとめる。
    """

    def build(
        self,
        *,
        chart,
        element_strength,
        kakukyoku=None,
        yojin=None,
        combinations=None,
        house_gods=None,
        ai_reading=None,
    ) -> PaperReport:

        return PaperReport(
            chart=chart,
            element_strength=element_strength,
            kakukyoku=kakukyoku,
            yojin=yojin,
            combinations=combinations,
            house_gods=house_gods,
            ai_reading=ai_reading,
        )