from dataclasses import dataclass


@dataclass(frozen=True)
class AIReading:
    summary: str
    personality: str
    fortune: str
    advice: str


class AIReadingAnalyzer:
    """
    AIへ渡す鑑定データ生成

    OpenAI
    Gemini
    Claude

    の共通インターフェース。
    """

    def build_prompt(self, chart):

        return {
            "chart": chart,
        }

    def analyze(self, chart):

        return AIReading(
            summary="",
            personality="",
            fortune="",
            advice="",
        )