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
    """
    鑑定書生成クラス

    Chart
        ↓
    各Analyzer
        ↓
    PaperReport
    """

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

    # ------------------------------------------------------------
    # 鑑定書生成
    # ------------------------------------------------------------

    def build(self, chart) -> PaperReport:

        # 五行
        element = self.element.analyze(chart)

        # 格局
        kakukyoku = self.kakukyoku.analyze(
            chart,
            element,
        )

        # 用神
        yojin = self.yojin.analyze(
            chart,
            element,
            kakukyoku,
        )

        # 宮位
        house = self.house.analyze(chart)

        # 合・冲・刑・害・方合・三合
        combo = self.combo.analyze(chart)

        # 大運
        taiun = self.taiun.analyze(chart)

        # 流年
        ryunen = self.ryunen.analyze(chart)

        # 流月
        ryugetsu = self.ryugetsu.analyze(chart)

        # 流日
        ryunichi = self.ryunichi.analyze(chart)

        # AI鑑定
        reading = self.ai.analyze(
            chart,
            element,
            kakukyoku,
            yojin,
            combo,
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