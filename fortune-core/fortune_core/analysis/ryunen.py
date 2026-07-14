from dataclasses import dataclass


@dataclass(frozen=True)
class RyunenRow:
    year: int
    kanchi: str


class RyunenAnalyzer:

    def analyze(
        self,
        start_year: int,
        end_year: int,
    ):
        """
        流年一覧生成

        六十干支計算は後で追加。
        """
        return []