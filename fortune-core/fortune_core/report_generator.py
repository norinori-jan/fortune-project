"""
report_generator.py
===================

髑大ｮ夂ｵ先棡繧単DF/逕ｻ蜒・JSON蠖｢蠑上〒逕滓・繝ｻ菫晏ｭ倥☆繧九Δ繧ｸ繝･繝ｼ繝ｫ縲・
繝ｦ繝ｼ繧ｶ繝ｼ縺後瑚・蛻・・雉・肇縲阪→縺励※謖√■蟶ｰ繧翫∵､懆ｨｼ繝ｻ蜿ら・縺ｧ縺阪ｋ繝ｬ繝昴・繝医ｒ菴懈・縲・

荳ｻ隕∵ｩ溯・:
- 繧ｿ繝ｭ繝・ヨ髑大ｮ夂ｵ先棡繧谷SON蠖｢蠑上〒菫晏ｭ・
- 逕ｻ蜒丞ｽ｢蠑擾ｼ・NG/JPEG・峨〒繝薙ず繝･繧｢繝ｫ繝ｬ繝昴・繝育函謌・
- PDF蠖｢蠑上〒繝励Ο蜩∬ｳｪ繝ｬ繝昴・繝育函謌・
- 繝ｭ繝ｼ繧ｫ繝ｫ繝輔ぃ繧､繝ｫ菫晏ｭ倥う繝ｳ繧ｿ繝ｼ繝輔ぉ繝ｼ繧ｹ
"""

import json
import io
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional, Literal
from urllib.parse import urlencode
import base64


# ---------------------------------------------------------------------------
# 繝・・繧ｿ繧ｯ繝ｩ繧ｹ
# ---------------------------------------------------------------------------


@dataclass
class ReadingReport:
    """髑大ｮ壹Ξ繝昴・繝・""
    reading_id: str
    query_text: str
    timestamp: str
    divination_type: str
    positions: dict
    element_distribution: dict
    user_seed: Optional[int]
    custom_meanings: dict = None

    def __post_init__(self):
        if self.custom_meanings is None:
            self.custom_meanings = {}

    def to_dict(self) -> dict:
        """JSON 繧ｷ繝ｪ繧｢繝ｩ繧､繧ｺ"""
        return {
            "reading_id": self.reading_id,
            "query_text": self.query_text,
            "timestamp": self.timestamp,
            "divination_type": self.divination_type,
            "positions": self.positions,
            "element_distribution": self.element_distribution,
            "user_seed": self.user_seed,
            "custom_meanings": self.custom_meanings,
        }


# ---------------------------------------------------------------------------
# 繝ｬ繝昴・繝育函謌舌お繝ｳ繧ｸ繝ｳ
# ---------------------------------------------------------------------------


class ReportGenerator:
    """
    髑大ｮ夂ｵ先棡繧偵・繝ｫ繝√ヵ繧ｩ繝ｼ繝槭ャ繝茨ｼ・SON/HTML/PDF/Image・峨〒逕滓・繝ｻ菫晏ｭ倥☆繧九・
    """

    def __init__(self):
        """蛻晄悄蛹・""
        pass

    def generate_json_report(self, report: ReadingReport) -> str:
        """
        JSON 蠖｢蠑上・繝ｬ繝昴・繝医ｒ逕滓・・医ユ繧ｭ繧ｹ繝茨ｼ峨・

        Returns
        -------
        str
            JSON 譁・ｭ怜・
        """
        return json.dumps(report.to_dict(), ensure_ascii=False, indent=2)

    def save_json_report(
        self,
        report: ReadingReport,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        JSON 繝ｬ繝昴・繝医ｒ繝輔ぃ繧､繝ｫ縺ｫ菫晏ｭ倥・

        Parameters
        ----------
        report : ReadingReport
            髑大ｮ壹Ξ繝昴・繝・
        output_path : Path | None
            菫晏ｭ伜・繝代せ縲・one 縺ｮ蝣ｴ蜷医・繝帙・繝繝・ぅ繝ｬ繧ｯ繝医Μ/fortune_readings 縺ｫ菫晏ｭ倥・

        Returns
        -------
        Path
            螳滄圀縺ｮ菫晏ｭ伜・繝代せ
        """
        if output_path is None:
            output_dir = Path.home() / "fortune_readings" / "json"
            output_path = output_dir / f"{report.reading_id}.json"
        else:
            output_path = Path(output_path)
        
        # 隕ｪ繝・ぅ繝ｬ繧ｯ繝医Μ繧剃ｽ懈・
        output_path.parent.mkdir(parents=True, exist_ok=True)

        json_text = self.generate_json_report(report)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_text)

        return output_path

    def generate_html_report(self, report: ReadingReport) -> str:
        """
        HTML 蠖｢蠑上・繝薙ず繝･繧｢繝ｫ繝ｬ繝昴・繝医ｒ逕滓・縲・
        繝悶Λ繧ｦ繧ｶ縺ｧ髢九＞縺溘ｊ縲√せ繧ｯ繝ｪ繝ｼ繝ｳ繧ｷ繝ｧ繝・ヨ縺ｧ逕ｻ蜒丞喧縺ｧ縺阪ｋ縲・

        Returns
        -------
        str
            HTML 譁・ｭ怜・・医ヵ繝ｫ繝峨く繝･繝｡繝ｳ繝茨ｼ・
        """
        positions_html = self._generate_positions_html(report.positions)
        element_dist_html = self._generate_element_distribution_html(
            report.element_distribution
        )

        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>繧ｿ繝ｭ繝・ヨ髑大ｮ壹Ξ繝昴・繝・- {report.reading_id}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Georgia', 'Noto Sans JP', serif;
            background: linear-gradient(135deg, #1a0033 0%, #2d0052 100%);
            color: #d0d0d0;
            padding: 20px;
            line-height: 1.6;
        }}
        
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background: rgba(20, 10, 40, 0.95);
            border: 2px solid #9333ea;
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 0 30px rgba(147, 51, 234, 0.3);
        }}
        
        header {{
            text-align: center;
            border-bottom: 2px solid #9333ea;
            padding-bottom: 30px;
            margin-bottom: 40px;
        }}
        
        h1 {{
            font-size: 32px;
            color: #d8b4fe;
            margin-bottom: 10px;
            font-weight: normal;
        }}
        
        .reading-meta {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
            padding: 20px;
            background: rgba(147, 51, 234, 0.1);
            border-radius: 8px;
            border-left: 4px solid #9333ea;
        }}
        
        .meta-item {{
            display: flex;
            flex-direction: column;
        }}
        
        .meta-label {{
            font-size: 12px;
            color: #a78bfa;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 4px;
        }}
        
        .meta-value {{
            font-size: 14px;
            color: #d8b4fe;
            font-weight: bold;
        }}
        
        .query-box {{
            background: rgba(147, 51, 234, 0.15);
            border-left: 4px solid #a855f7;
            padding: 15px;
            margin-bottom: 30px;
            border-radius: 4px;
        }}
        
        .query-label {{
            font-size: 12px;
            color: #a78bfa;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}
        
        .query-text {{
            font-size: 16px;
            color: #e9d5ff;
            font-style: italic;
        }}
        
        section {{
            margin-bottom: 40px;
        }}
        
        section h2 {{
            font-size: 20px;
            color: #d8b4fe;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #5d28a8;
            font-weight: normal;
        }}
        
        .positions-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }}
        
        .card-position {{
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid #6366f1;
            border-radius: 8px;
            padding: 15px;
            position: relative;
        }}
        
        .card-position.upright {{
            border-left: 4px solid #06b6d4;
        }}
        
        .card-position.reversed {{
            border-left: 4px solid #f87171;
            opacity: 0.85;
        }}
        
        .position-index {{
            font-size: 11px;
            color: #a78bfa;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}
        
        .position-name {{
            font-size: 14px;
            font-weight: bold;
            color: #d8b4fe;
            margin-bottom: 8px;
        }}
        
        .card-name {{
            font-size: 16px;
            color: #e9d5ff;
            margin-bottom: 6px;
            font-style: italic;
        }}
        
        .card-element {{
            display: inline-block;
            font-size: 11px;
            padding: 4px 8px;
            background: rgba(147, 51, 234, 0.3);
            border-radius: 4px;
            color: #a78bfa;
            margin-right: 6px;
            margin-bottom: 10px;
        }}
        
        .card-orientation {{
            font-size: 12px;
            color: #06b6d4;
            margin-bottom: 8px;
        }}
        
        .card-orientation.reversed {{
            color: #f87171;
        }}
        
        .card-meaning {{
            font-size: 12px;
            color: #c7d2fe;
            line-height: 1.5;
            padding-top: 8px;
            border-top: 1px solid #5d28a8;
        }}
        
        .element-distribution {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 15px;
        }}
        
        .element-card {{
            background: rgba(99, 102, 241, 0.1);
            border: 1px solid #6366f1;
            border-radius: 8px;
            padding: 15px;
            text-align: center;
        }}
        
        .element-icon {{
            font-size: 32px;
            margin-bottom: 8px;
        }}
        
        .element-count {{
            font-size: 24px;
            font-weight: bold;
            color: #d8b4fe;
            margin-bottom: 4px;
        }}
        
        .element-name {{
            font-size: 12px;
            color: #a78bfa;
        }}
        
        footer {{
            border-top: 2px solid #9333ea;
            padding-top: 20px;
            margin-top: 40px;
            text-align: center;
            font-size: 11px;
            color: #6b7280;
        }}
        
        .footer-text {{
            margin-bottom: 8px;
        }}
        
        .print-instruction {{
            text-align: center;
            margin-top: 20px;
            font-size: 12px;
            color: #a78bfa;
        }}
        
        @media print {{
            body {{
                background: white;
                color: black;
            }}
            
            .container {{
                background: white;
                border: none;
                box-shadow: none;
            }}
            
            .print-instruction {{
                display: none;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>醗 繧ｿ繝ｭ繝・ヨ髑大ｮ壹Ξ繝昴・繝・/h1>
        </header>
        
        <div class="reading-meta">
            <div class="meta-item">
                <span class="meta-label">Reading ID</span>
                <span class="meta-value">{report.reading_id}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">髑大ｮ壽律譎・/span>
                <span class="meta-value">{datetime.fromisoformat(report.timestamp).strftime('%Y蟷ｴ%m譛・d譌･ %H:%M')}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">蜊陦・/span>
                <span class="meta-value">{report.divination_type}</span>
            </div>
            <div class="meta-item">
                <span class="meta-label">繧ｷ繝ｳ繧ｯ繝ｭ繧ｷ繝ｼ繝・/span>
                <span class="meta-value">{report.user_seed if report.user_seed else '繝ｩ繝ｳ繝繝'}</span>
            </div>
        </div>
        
        <div class="query-box">
            <div class="query-label">逶ｸ隲・・螳ｹ</div>
            <div class="query-text">縲鶏report.query_text}縲・/div>
        </div>
        
        <section>
            <h2>島 繧ｱ繝ｫ繝亥香蟄励せ繝励Ξ繝・ラ・・0譫夲ｼ・/h2>
            <div class="positions-grid">
                {positions_html}
            </div>
        </section>
        
        <section>
            <h2>笞｡ 隕∫ｴ繝舌Λ繝ｳ繧ｹ蛻・梵</h2>
            <div class="element-distribution">
                {element_dist_html}
            </div>
        </section>
        
        <footer>
            <div class="footer-text">
                縺薙・繝ｬ繝昴・繝医・ fortune-core 縺ｫ繧医▲縺ｦ閾ｪ蜍慕函謌舌＆繧後∪縺励◆縲・
            </div>
            <div class="footer-text">
                繧ｫ繝ｼ繝芽ｧ｣驥医・蜿り・ュ蝣ｱ縺ｧ縺吶よ怙邨ら噪縺ｪ蛻､譁ｭ縺ｯ縺碑・霄ｫ縺ｮ逶ｴ諢溘→邨碁ｨ薙ｒ蜆ｪ蜈医＠縺ｦ縺上□縺輔＞縲・
            </div>
            <div class="print-instruction">
                沈 縺薙・繝壹・繧ｸ繧偵ヶ繝ｩ繧ｦ繧ｶ縺ｮ繧ｹ繧ｯ繝ｪ繝ｼ繝ｳ繧ｷ繝ｧ繝・ヨ讖溯・縺ｧ逕ｻ蜒丈ｿ晏ｭ倥☆繧九°縲・
                Ctrl+P 縺ｧ PDF 縺ｨ縺励※菫晏ｭ倥〒縺阪∪縺吶・
            </div>
        </footer>
    </div>
    
    <script>
        // 繝壹・繧ｸ繝ｭ繝ｼ繝牙ｮ御ｺ・凾縺ｫ繝｡繝・そ繝ｼ繧ｸ陦ｨ遉ｺ・医ョ繝｢逕ｨ・・
        window.addEventListener('load', () => {{
            console.log('Report loaded. Use Ctrl+P to save as PDF or take a screenshot.');
        }});
    </script>
</body>
</html>"""

        return html

    def _generate_positions_html(self, positions: dict) -> str:
        """繝昴ず繧ｷ繝ｧ繝ｳ諠・ｱ繧辿TML縺ｧ逕滓・"""
        html_parts = []
        for pos_key, pos_data in positions.items():
            card = pos_data.get("card", {})
            is_reversed = pos_data.get("is_reversed", False)
            orientation = "reversed" if is_reversed else "upright"

            element = card.get("element", "unknown")
            element_emoji = {
                "fire": "櫨",
                "water": "挑",
                "air": "軒",
                "earth": "諺",
                "spirit": "笨ｨ",
            }.get(element, "笨ｦ")

            card_html = f"""<div class="card-position {orientation}">
                <div class="position-index">Position {pos_data.get('position_index', '?')}</div>
                <div class="position-name">{pos_data.get('position_label', 'Unknown')}</div>
                <div class="card-name">{card.get('name', 'Unknown Card')}</div>
                <div>
                    <span class="card-element">{element_emoji} {element.upper()}</span>
                </div>
                <div class="card-orientation {'reversed' if is_reversed else ''}">
                    {'売 騾・ｽ咲ｽｮ・・eversed・・ if is_reversed else '笨・豁｣菴咲ｽｮ・・pright・・}
                </div>
                <div class="card-meaning">
                    {card.get('meaning_upright' if not is_reversed else 'meaning_reversed', 'No meaning available')}
                </div>
            </div>"""
            html_parts.append(card_html)

        return "\n".join(html_parts)

    def _generate_element_distribution_html(self, distribution: dict) -> str:
        """隕∫ｴ蛻・ｸ・ｒHTML縺ｧ逕滓・"""
        element_emojis = {
            "fire": "櫨",
            "water": "挑",
            "air": "軒",
            "earth": "諺",
            "spirit": "笨ｨ",
        }

        html_parts = []
        for element, count in distribution.items():
            emoji = element_emojis.get(element, "笨ｦ")
            html_part = f"""<div class="element-card">
                <div class="element-icon">{emoji}</div>
                <div class="element-count">{count}</div>
                <div class="element-name">{element.upper()}</div>
            </div>"""
            html_parts.append(html_part)

        return "\n".join(html_parts)

    def save_html_report(
        self,
        report: ReadingReport,
        output_path: Optional[Path] = None,
    ) -> Path:
        """
        HTML 繝ｬ繝昴・繝医ｒ繝輔ぃ繧､繝ｫ縺ｫ菫晏ｭ倥・

        Returns
        -------
        Path
            螳滄圀縺ｮ菫晏ｭ伜・繝代せ
        """
        if output_path is None:
            output_dir = Path.home() / "fortune_readings" / "html"
            output_path = output_dir / f"{report.reading_id}.html"
        else:
            output_path = Path(output_path)
        
        # 隕ｪ繝・ぅ繝ｬ繧ｯ繝医Μ繧剃ｽ懈・
        output_path.parent.mkdir(parents=True, exist_ok=True)

        html_text = self.generate_html_report(report)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_text)

        return output_path

    def generate_share_url(
        self,
        report: ReadingReport,
        base_url: str = "https://fortune-core.example.com/reading",
    ) -> str:
        """
        髑大ｮ夂ｵ先棡繧偵す繧ｧ繧｢蜿ｯ閭ｽ縺ｪURL縺ｫ螟画鋤縲・
        繧ｯ繧ｨ繝ｪ繝代Λ繝｡繝ｼ繧ｿ縺ｫ繝ｬ繝昴・繝医ョ繝ｼ繧ｿ繧定ｩｰ繧√※霑斐☆縲・

        Parameters
        ----------
        report : ReadingReport
            髑大ｮ壹Ξ繝昴・繝・
        base_url : str
            繝吶・繧ｹURL・医ョ繝輔か繝ｫ繝医・繝励Ξ繝ｼ繧ｹ繝帙Ν繝繝ｼ・・

        Returns
        -------
        str
            繧ｷ繧ｧ繧｢URL
        """
        report_json = json.dumps(report.to_dict())
        encoded = base64.b64encode(report_json.encode("utf-8")).decode("utf-8")
        params = {"data": encoded}
        return f"{base_url}?{urlencode(params)}"

    def export_formats(
        self,
        report: ReadingReport,
        output_dir: Optional[Path] = None,
        formats: tuple[Literal["json", "html"], ...] = ("json", "html"),
    ) -> dict[str, Path]:
        """
        隍・焚蠖｢蠑上〒蜷梧凾繧ｨ繧ｯ繧ｹ繝昴・繝医・

        Parameters
        ----------
        report : ReadingReport
            髑大ｮ壹Ξ繝昴・繝・
        output_dir : Path | None
            蜃ｺ蜉帙ョ繧｣繝ｬ繧ｯ繝医Μ・・one縺ｮ蝣ｴ蜷医・閾ｪ蜍包ｼ・
        formats : tuple
            蜃ｺ蜉帛ｽ｢蠑擾ｼ・json', 'html'・・

        Returns
        -------
        dict[str, Path]
            蠖｢蠑上＃縺ｨ縺ｮ菫晏ｭ伜・繝代せ
        """
        if output_dir is None:
            output_dir = Path.home() / "fortune_readings"

        results = {}

        if "json" in formats:
            json_path = self.save_json_report(report, output_dir / "json" / f"{report.reading_id}.json")
            results["json"] = json_path

        if "html" in formats:
            html_path = self.save_html_report(report, output_dir / "html" / f"{report.reading_id}.html")
            results["html"] = html_path

        return results

    def get_save_instructions(self) -> str:
        """
        繝ｦ繝ｼ繧ｶ繝ｼ縺ｸ縺ｮ菫晏ｭ俶婿豕輔ぎ繧､繝峨ｒ霑斐☆縲・
        """
        return """
縲宣荘螳夂ｵ先棡縺ｮ菫晏ｭ俶婿豕輔・

導 繧ｹ繝槭・繝医ヵ繧ｩ繝ｳ・・Phone/Android・・
  1. HTML繝ｬ繝昴・繝医ｒ繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥
  2. 縲悟・譛峨阪・繧ｿ繝ｳ繧偵ち繝・・
  3. 縲後ヵ繧｡繧､繝ｫ縺ｫ菫晏ｭ倥阪∪縺溘・縲悟・逵溘↓菫晏ｭ倥阪ｒ驕ｸ謚・
  4. 螳御ｺ・ｼ・

捗 PC・・indows/Mac・・
  1. HTML繝ｬ繝昴・繝医ｒ繝悶Λ繧ｦ繧ｶ縺ｧ髢九￥
  2. Ctrl+P・医∪縺溘・Cmd+P・峨〒蜊ｰ蛻ｷ繝繧､繧｢繝ｭ繧ｰ繧帝幕縺・
  3. 縲訓DF縺ｫ菫晏ｭ倥阪ｒ驕ｸ謚・
  4. 縺ｾ縺溘・ Ctrl+S・医∪縺溘・Cmd+S・峨〒HTML蠖｢蠑上〒菫晏ｭ・

投 繝・・繧ｿ繝舌ャ繧ｯ繧｢繝・・:
  - JSON蠖｢蠑上Ξ繝昴・繝医・螳悟・縺ｪ繝・・繧ｿ繧剃ｿ晄戟縺励※縺翫ｊ縲・
    蠕後°繧牙挨繧ｷ繧ｹ繝・Β縺ｫ繧､繝ｳ繝昴・繝医〒縺阪∪縺吶・
  - 菫晏ｭ伜・: {Path.home() / 'fortune_readings'}
"""
