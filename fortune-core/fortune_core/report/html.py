# fortune_core/report/html.py

from html import escape

from .models import PaperReport


class HTMLReportBuilder:
    """
    PaperReport → HTML

    HTMLテンプレート生成クラス。
    将来的には Jinja2 テンプレートへ置き換え可能。
    """

    def build(self, report: PaperReport) -> str:

        chart = report.chart

        def pillar(pillar):

            return f"""
            <td>
                <div><strong>{escape(pillar.stem.name)}</strong></div>
                <div>{escape(pillar.branch.name)}</div>
            </td>
            """

        html = f"""
<!DOCTYPE html>

<html lang="ja">

<head>

<meta charset="utf-8">

<title>四柱推命鑑定書</title>

<style>

body {{

    font-family: sans-serif;
    margin:40px;
    line-height:1.8;

}}

h1 {{

    border-bottom:2px solid #333;

}}

table {{

    width:100%;
    border-collapse:collapse;

}}

th,td {{

    border:1px solid #999;
    padding:8px;
    text-align:center;

}}

.section {{

    margin-top:35px;

}}

</style>

</head>

<body>

<h1>四柱推命鑑定書</h1>

<div class="section">

<h2>命式</h2>

<table>

<tr>

<th>年柱</th>
<th>月柱</th>
<th>日柱</th>
<th>時柱</th>

</tr>

<tr>

{pillar(chart.year)}
{pillar(chart.month)}
{pillar(chart.day)}
{pillar(chart.hour)}

</tr>

</table>

</div>

<div class="section">

<h2>五行量</h2>

<ul>

{''.join(
f"<li>{escape(str(k))} ： {escape(str(v))}</li>"
for k, v in report.element_strength.values.items()
)}

</ul>

</div>

<div class="section">

<h2>格局</h2>

<p>

{
escape(report.kakukyoku.name)
if report.kakukyoku
else "未判定"
}

</p>

</div>

<div class="section">

<h2>用神</h2>

<p>

{
escape(report.yojin.main)
if report.yojin
else "未判定"
}

</p>

</div>

<div class="section">

<h2>会局・方合</h2>

<p>

方合：
{
escape(report.combinations.hogo)
if report.combinations and report.combinations.hogo
else "なし"
}

</p>

<p>

会局：
{
escape(report.combinations.kaikyoku)
if report.combinations and report.combinations.kaikyoku
else "なし"
}

</p>

</div>

<div class="section">

<h2>神殺・宮位</h2>

<table>

<tr>

<th>年柱</th>
<th>月柱</th>
<th>日柱</th>
<th>時柱</th>

</tr>

<tr>

<td>{", ".join(report.house_gods.year.gods)}</td>

<td>{", ".join(report.house_gods.month.gods)}</td>

<td>{", ".join(report.house_gods.day.gods)}</td>

<td>{", ".join(report.house_gods.hour.gods)}</td>

</tr>

</table>

</div>

<div class="section">

<h2>AI総合鑑定</h2>

<h3>総評</h3>

<p>{escape(report.ai_reading.summary)}</p>

<h3>性格</h3>

<p>{escape(report.ai_reading.personality)}</p>

<h3>才能</h3>

<p>{escape(report.ai_reading.talent)}</p>

<h3>仕事運</h3>

<p>{escape(report.ai_reading.work)}</p>

<h3>恋愛・結婚運</h3>

<p>{escape(report.ai_reading.love)}</p>

<h3>健康運</h3>

<p>{escape(report.ai_reading.health)}</p>

<h3>運勢</h3>

<p>{escape(report.ai_reading.fortune)}</p>

<h3>アドバイス</h3>

<p>{escape(report.ai_reading.advice)}</p>

</div>

</body>

</html>
"""

        return html