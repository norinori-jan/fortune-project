from datetime import datetime
from fortune_core.shichu.dataclasses import Chart, TaiunRow, NenunCell
from fortune_core.shichu.engine import Engine

class AIReading:
    """
    命式＋運勢を総合して鑑定文を生成する層。
    Chart と Engine を使って文章を返す。
    """

    def summarize_meishiki(self, chart: Chart) -> str:
        kk = chart.analysis.kakukyoku or "通常格"
        yj = chart.analysis.yojin or "特定なし"
        choko = chart.analysis.choko or "特別な調候補正なし"

        return (
            f"【命式の性質】\n"
            f"・格局：{kk}\n"
            f"・用神：{yj}\n"
            f"・調候：{choko}\n"
        )

    def summarize_taiun(self, chart: Chart, taiun: TaiunRow) -> str:
        return (
            f"【大運のテーマ】\n"
            f"・大運干支：{taiun.taiun_kanchi}\n"
            f"・通変星：{taiun.taiun_ten_god.name}\n"
            f"・十二運：{taiun.taiun_twelve_growth.name}\n"
        )

    def summarize_nenun(self, nen: NenunCell, chart: Chart) -> str:
        tg = chart.ten_gods_engine.get_ten_god(
            chart.day.stem,
            chart.tenkan_engine.registry_loader.get_stems()[nen.kanchi[0]]
        )
        return (
            f"【流年のテーマ（{nen.seireki}年）】\n"
            f"・年干支：{nen.kanchi}\n"
            f"・通変星：{tg.name}\n"
            f"・十二運：{nen.twelve_growth.name}\n"
        )

    def full_reading(self, chart: Chart, engine: Engine, target_year: int, target_month: int, target_date: datetime) -> str:
        meishiki = self.summarize_meishiki(chart)

        taiun = engine.get_current_taiun(chart, target_date)
        taiun_text = self.summarize_taiun(chart, taiun) if taiun else "大運情報なし\n"

        nen = engine.get_nenun(chart, target_year)
        nen_text = self.summarize_nenun(nen, chart) if nen else "流年情報なし\n"

        return (
            "==============================\n"
            "　　　【総合鑑定】\n"
            "==============================\n\n"
            + meishiki + "\n"
            + taiun_text + "\n"
            + nen_text + "\n"
        )

