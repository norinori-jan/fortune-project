from datetime import datetime
from fortune_core.shichu.dataclasses import Chart
from fortune_core.shichu.engine import Engine

class AIQA:
    """
    ユーザーの質問に応じて、命式＋運勢から回答を生成する層。
    """

    def __init__(self, engine: Engine):
        self.engine = engine

    def classify(self, question: str) -> str:
        q = question
        if "仕事" in q: return "work"
        if "恋愛" in q: return "love"
        if "健康" in q: return "health"
        if "金運" in q: return "money"
        if "大運" in q: return "taiun"
        if "今年" in q or "流年" in q: return "nenun"
        return "general"

    def answer(self, chart: Chart, question: str, today: datetime) -> str:
        field = self.classify(question)
        year = today.year

        if field == "taiun":
            taiun = self.engine.get_current_taiun(chart, today)
            return f"現在の大運は {taiun.taiun_kanchi} です。" if taiun else "大運情報なし。"

        if field == "nenun":
            nen = self.engine.get_nenun(chart, year)
            return f"{year}年の流年は {nen.kanchi} です。" if nen else "流年情報なし。"

        if field == "work":
            return f"{year}年の仕事運は、流年の象意がキャリア面に影響します。"
        if field == "love":
            return f"{year}年の恋愛運は、流年の象意が人間関係に影響します。"
        if field == "health":
            return f"{year}年の健康運は、十二運の勢いが体調に影響します。"
        if field == "money":
            return f"{year}年の金運は、通変星の象意が財の動きに影響します。"

        return "もう少し具体的に質問してください。"

