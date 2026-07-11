from fortune_core.shichu.dataclasses import Chart

class AIExplain:
    """
    命式の各要素を自然言語で説明する層。
    Chart を入力にして文章を返す。
    """

    def explain_kakukyoku(self, chart: Chart) -> str:
        kk = chart.analysis.kakukyoku
        if not kk:
            return "この命式には特別な格局は見られません。日主の強弱と五行の配置に基づく通常の判断となります。"

        return f"この命式は「{kk}」に該当します。従格は日主の力が極端に弱く、他の五行が強く支配することで成立します。"

    def explain_yojin(self, chart: Chart) -> str:
        yj = chart.analysis.yojin
        if not yj:
            return "用神は特定されていません。五行の偏りが小さく、全体のバランスを重視する命式です。"

        return f"この命式の用神は「{yj}」です。五行の偏りを補い、命式全体の調和を保つ重要な要素です。"

    def explain_choko(self, chart: Chart) -> str:
        ck = chart.analysis.choko
        if not ck:
            return "調候上の大きな偏りはありません。季節の気に対して特別な補正は不要です。"

        return f"調候では「{ck}」が必要とされます。これは季節の寒暖・湿燥に応じて五行の補正を行うためです。"

    def explain_special(self, chart: Chart) -> str:
        sp = chart.special_combinations
        msgs = []

        if sp.nichigan_heirin_year:
            msgs.append(f"日干併臨が {sp.nichigan_heirin_year} 年に巡ります。日主の象意が強く現れやすい年です。")

        if sp.getsugan_heirin_year:
            msgs.append(f"月干併臨が {sp.getsugan_heirin_year} 年に巡ります。月柱の象意が強く現れやすい年です。")

        if sp.tenchi_tokugo_year:
            msgs.append(f"天地徳合が {sp.tenchi_tokugo_year} 年に成立します。非常に吉祥で、調和と幸運が強まる年です。")

        if not msgs:
            return "特殊干支の併臨や天地徳合は見られません。"

        return " ".join(msgs)

    def explain_element_balance(self, chart: Chart) -> str:
        vals = chart.element_strength.values
        msg = "【五行バランス】\n"
        for k, v in vals.items():
            msg += f"・{k}: {v}\n"

        return msg + "五行の偏りをもとに、用神や調候が判断されます。"

    def explain_all(self, chart: Chart) -> str:
        parts = [
            self.explain_kakukyoku(chart),
            self.explain_yojin(chart),
            self.explain_choko(chart),
            self.explain_special(chart),
            self.explain_element_balance(chart),
        ]
        return "\n\n".join(parts)
