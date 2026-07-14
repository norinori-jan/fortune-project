from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class RyunichiRow:
    day: date
    kanchi: str


class RyunichiAnalyzer:

    def analyze(
        self,
        year: int,
        month: int,
    ):
        """
        流日生成

        日干支計算は後で追加。
        """
        return []