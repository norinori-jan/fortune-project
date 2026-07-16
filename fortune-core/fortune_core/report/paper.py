from fortune_core.analysis.element_strength import ElementStrengthAnalyzer
from fortune_core.analysis.kakukyoku import KakukyokuAnalyzer
from fortune_core.analysis.yojin import YojinAnalyzer
from fortune_core.analysis.house_gods import HouseGodsAnalyzer
from fortune_core.analysis.combinations import CombinationAnalyzer
from fortune_core.analysis.taiun import TaiunAnalyzer
from fortune_core.analysis.ryunen import RyunenAnalyzer
from fortune_core.analysis.ryugetsu import RyugetsuAnalyzer
from fortune_core.analysis.ryunichi import RyunichiAnalyzer
from fortune_core.analysis.ai_reading import AIReadingAnalyzer

from .models import PaperReport


class PaperBuilder:

    def __init__(self):

        self.element = ElementStrengthAnalyzer()
        self.kakukyoku = KakukyokuAnalyzer()
        self.yojin = YojinAnalyzer()
        self.house = HouseGodsAnalyzer()
        self.combo = CombinationAnalyzer()
        self.taiun = TaiunAnalyzer()
        self.ryunen = RyunenAnalyzer()
        self.ryugetsu = RyugetsuAnalyzer()
        self.ryunichi = RyunichiAnalyzer()
        self.ai = AIReadingAnalyzer()

    def build(self, chart):

        element = self.element.analyze(chart)

        kakukyoku = self.kakukyoku.analyze(
            chart,
            element
        )

        yojin = self.yojin.analyze(
            chart,
            element,
            kakukyoku
        )

        house = self.house.analyze(chart)

        combo = self.combo.analyze(chart)

        taiun = self.taiun.analyze(chart)

        ryunen = self.ryunen.analyze(chart)

        ryugetsu = self.ryugetsu.analyze(chart)

        ryunichi = self.ryunichi.analyze(chart)

        reading = self.ai.analyze(
            chart,
            element,
            kakukyoku,
            yojin,
            combo
        )

        return PaperReport(
            chart=chart,
            element_strength=element,
            kakukyoku=kakukyoku,
            yojin=yojin,
            house_gods=house,
            combinations=combo,
            taiun=taiun,
            ryunen=ryunen,
            ryugetsu=ryugetsu,
            ryunichi=ryunichi,
            ai_reading=reading,
        )