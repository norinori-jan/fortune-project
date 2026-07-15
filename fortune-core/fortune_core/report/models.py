from dataclasses import dataclass
from typing import Optional

from fortune_core.shichu.dataclasses import Chart
from fortune_core.analysis.element_strength import ElementStrength
from fortune_core.analysis.kakukyoku import KakukyokuResult
from fortune_core.analysis.yojin import YojinResult
from fortune_core.analysis.house_gods import HouseGodsResult
from fortune_core.analysis.combinations import CombinationResult


@dataclass
class PaperReport:
    """
    鑑定書全体
    """

    chart: Chart

    element_strength: Optional[ElementStrength] = None

    combinations: Optional[CombinationResult] = None

    kakukyoku: Optional[KakukyokuResult] = None

    yojin: Optional[YojinResult] = None

    house_gods: Optional[HouseGodsResult] = None