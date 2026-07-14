# fortune_core/analysis/house_gods.py

from dataclasses import dataclass, field


@dataclass(frozen=True)
class HouseGod:
    """
    各宮位（年・月・日・時）に付与される神や情報
    """

    house: str
    gods: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class HouseGodResult:
    """
    鑑定書で使用する十二宮情報
    """

    year: HouseGod
    month: HouseGod
    day: HouseGod
    hour: HouseGod


class HouseGodAnalyzer:
    """
    宮位ごとの神をまとめるクラス

    現段階では GodsEngine の結果を
    鑑定書で扱いやすい形式へ変換するだけ。
    """

    def analyze(self, chart) -> HouseGodResult:

        gods = chart.house_gods

        return HouseGodResult(
            year=HouseGod(
                house="年柱",
                gods=[g.name for g in gods.get("year", [])],
            ),
            month=HouseGod(
                house="月柱",
                gods=[g.name for g in gods.get("month", [])],
            ),
            day=HouseGod(
                house="日柱",
                gods=[g.name for g in gods.get("day", [])],
            ),
            hour=HouseGod(
                house="時柱",
                gods=[g.name for g in gods.get("hour", [])],
            ),
        )