# fortune_core/analysis/house_gods.py

from dataclasses import dataclass


@dataclass(frozen=True)
class HouseGod:
    """
    宮位情報
    """

    name: str
    pillar: str
    stem: str
    branch: str
    description: str


@dataclass(frozen=True)
class HouseGodsResult:
    """
    十二宮（四柱版）
    """

    year: HouseGod
    month: HouseGod
    day: HouseGod
    hour: HouseGod


class HouseGodsAnalyzer:
    """
    宮位解析

    年柱＝祖先・家系・幼少期
    月柱＝父母・兄弟・青年期
    日柱＝本人・配偶者・壮年期
    時柱＝子女・晩年
    """

    def analyze(self, chart) -> HouseGodsResult:

        return HouseGodsResult(
            year=self._build_year(chart),
            month=self._build_month(chart),
            day=self._build_day(chart),
            hour=self._build_hour(chart),
        )

    # ------------------------------------------------------------
    # 年柱
    # ------------------------------------------------------------

    def _build_year(self, chart):

        return HouseGod(
            name="年柱宮",
            pillar="year",
            stem=chart.year.stem.name,
            branch=chart.year.branch.name,
            description="祖先・家系・幼少期・社会背景",
        )

    # ------------------------------------------------------------
    # 月柱
    # ------------------------------------------------------------

    def _build_month(self, chart):

        return HouseGod(
            name="月柱宮",
            pillar="month",
            stem=chart.month.stem.name,
            branch=chart.month.branch.name,
            description="父母・兄弟姉妹・仕事・青年期",
        )

    # ------------------------------------------------------------
    # 日柱
    # ------------------------------------------------------------

    def _build_day(self, chart):

        return HouseGod(
            name="日柱宮",
            pillar="day",
            stem=chart.day.stem.name,
            branch=chart.day.branch.name,
            description="本人・配偶者・結婚運・壮年期",
        )

    # ------------------------------------------------------------
    # 時柱
    # ------------------------------------------------------------

    def _build_hour(self, chart):

        return HouseGod(
            name="時柱宮",
            pillar="hour",
            stem=chart.hour.stem.name,
            branch=chart.hour.branch.name,
            description="子女・部下・晩年運・未来",
        )