# fortune_core/analysis/ai_reading.py

from dataclasses import dataclass


@dataclass(frozen=True)
class AIReadingResult:
    """
    AI鑑定結果

    現在はテンプレート文章を返す。
    将来的には OpenAI / Gemini / Claude の出力を格納する。
    """

    summary: str
    personality: str
    talent: str
    work: str
    love: str
    health: str
    fortune: str
    advice: str


class AIReadingAnalyzer:
    """
    AI鑑定文章生成クラス

    現状
        RuleBase（テンプレート）

    将来
        OpenAI
        Gemini
        Claude

    へ差し替え可能。
    """

    # ------------------------------------------------------------
    # AIへ渡すデータ
    # ------------------------------------------------------------
    def build_prompt(
        self,
        chart,
        element,
        kakukyoku,
        yojin,
        combinations,
    ) -> dict:

        return {
            "chart": chart,
            "element_strength": element,
            "kakukyoku": kakukyoku,
            "yojin": yojin,
            "combinations": combinations,
        }

    # ------------------------------------------------------------
    # AI鑑定
    # ------------------------------------------------------------
    def analyze(
        self,
        chart,
        element,
        kakukyoku,
        yojin,
        combinations,
    ) -> AIReadingResult:

        # AIへ渡すデータ
        prompt = self.build_prompt(
            chart,
            element,
            kakukyoku,
            yojin,
            combinations,
        )

        # 現段階では使用しない（将来AIへ渡す）
        _ = prompt

        day_stem = chart.day.stem.name
        day_branch = chart.day.branch.name

        summary = (
            f"日主は「{day_stem}」、日支は「{day_branch}」です。"
            "命式全体のバランスから総合的に鑑定します。"
        )

        personality = (
            f"{day_stem}日主を中心とした性格・資質を読み取ります。"
        )

        talent = (
            "命式から適性・才能・得意分野を分析します。"
        )

        work = (
            "仕事運・適職・社会運を分析します。"
        )

        love = (
            "恋愛運・結婚運・家庭運を分析します。"
        )

        health = (
            "五行バランスから健康運を分析します。"
        )

        fortune = (
            "大運・流年を考慮した運勢を分析します。"
        )

        advice = (
            "用神・喜神を活用した開運方法を提案します。"
        )

        return AIReadingResult(
            summary=summary,
            personality=personality,
            talent=talent,
            work=work,
            love=love,
            health=health,
            fortune=fortune,
            advice=advice,
        )