from dataclasses import dataclass


@dataclass(frozen=True)
class RyugetsuRow:
    month: int
    kanchi: str


class RyugetsuAnalyzer:

    def analyze(
        self,
        year: int,
    ):
        """
        流月生成

        月建・節入り対応は後で追加。
        """
        return []