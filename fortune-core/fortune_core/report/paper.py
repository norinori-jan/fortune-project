from fortune_core.report.models import PaperReport

from fortune_core.analysis.element_strength import ElementStrengthAnalyzer
from fortune_core.analysis.combinations import CombinationAnalyzer
from fortune_core.analysis.kakukyoku import KakukyokuAnalyzer
from fortune_core.analysis.yojin import YojinAnalyzer
from fortune_core.analysis.house_gods import HouseGodsAnalyzer


class PaperBuilder:
    """
    四柱推命鑑定書ビルダー

    Engine.generate() が生成した Chart を受け取り、
    各解析モジュールを実行して PaperReport を生成する。
    """

    def __init__(self):
        self.element_strength = ElementStrengthAnalyzer()
        self.combinations = CombinationAnalyzer()
        self.kakukyoku = KakukyokuAnalyzer()
        self.yojin = YojinAnalyzer()
        self.house_gods = HouseGodsAnalyzer()

    def build(self, chart) -> PaperReport:
        """
        Chart → PaperReport
        """

        report = PaperReport(chart=chart)

        # ----------------------------------------------------
        # 五行量
        # ----------------------------------------------------
        report.element_strength = (
            self.element_strength.analyze(chart)
        )

        # ----------------------------------------------------
        # 合・冲・刑・害・三合・方合・会局
        # ----------------------------------------------------
        report.combinations = (
            self.combinations.analyze(chart)
        )

        # ----------------------------------------------------
        # 格局
        # ----------------------------------------------------
        report.kakukyoku = (
            self.kakukyoku.analyze(
                chart,
                report.element_strength,
            )
        )

        # ----------------------------------------------------
        # 用神・忌神
        # ----------------------------------------------------
        report.yojin = (
            self.yojin.analyze(
                chart,
                report.element_strength,
                report.kakukyoku,
            )
        )

        # ----------------------------------------------------
        # 十二宮・宮位神
        # ----------------------------------------------------
        report.house_gods = (
            self.house_gods.analyze(chart)
        )

        return report