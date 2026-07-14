from dataclasses import dataclass


@dataclass(frozen=True)
class TaiunRow:
    age: int
    kanchi: str
    start_year: int


class TaiunAnalyzer:

    def analyze(self, chart):
        """
        Engineから渡された命式を元に
        大運表を作成する。

        実ロジックは後で実装。
        """
        return []