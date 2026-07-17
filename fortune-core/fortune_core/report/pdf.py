# fortune_core/report/pdf.py

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .models import PaperReport


pdfmetrics.registerFont(
    UnicodeCIDFont("HeiseiMin-W3")
)


class PDFReportBuilder:
    """
    PaperReport → PDF
    """

    def build(
        self,
        report: PaperReport,
        output_path: str,
    ) -> None:

        styles = getSampleStyleSheet()

        style = styles["Normal"]
        style.fontName = "HeiseiMin-W3"

        doc = SimpleDocTemplate(output_path)

        elements = []

        # -------------------------------------------------
        # タイトル
        # -------------------------------------------------

        elements.append(
            Paragraph("四柱推命鑑定書", style)
        )

        elements.append(
            Spacer(1, 20)
        )

        # -------------------------------------------------
        # 命式
        # -------------------------------------------------

        chart = report.chart

        table = Table([
            ["", "年柱", "月柱", "日柱", "時柱"],
            [
                "天干",
                chart.year.stem.name,
                chart.month.stem.name,
                chart.day.stem.name,
                chart.hour.stem.name,
            ],
            [
                "地支",
                chart.year.branch.name,
                chart.month.branch.name,
                chart.day.branch.name,
                chart.hour.branch.name,
            ],
        ])

        table.setStyle(

            TableStyle([

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("FONTNAME", (0, 0), (-1, -1), "HeiseiMin-W3"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),

            ])

        )

        elements.append(table)

        elements.append(
            Spacer(1, 20)
        )

        # -------------------------------------------------
        # 五行量
        # -------------------------------------------------

        elements.append(
            Paragraph("【五行量】", style)
        )

        for element, value in report.element_strength.values.items():

            elements.append(
                Paragraph(
                    f"{element}：{value}",
                    style,
                )
            )

        elements.append(
            Spacer(1, 20)
        )

        # -------------------------------------------------
        # 格局
        # -------------------------------------------------

        elements.append(
            Paragraph("【格局】", style)
        )

        elements.append(
            Paragraph(
                report.kakukyoku.name
                if report.kakukyoku
                else "未判定",
                style,
            )
        )

        elements.append(
            Spacer(1, 20)
        )

        # -------------------------------------------------
        # 用神
        # -------------------------------------------------

        elements.append(
            Paragraph("【用神】", style)
        )

        elements.append(
            Paragraph(
                report.yojin.main
                if report.yojin
                else "未判定",
                style,
            )
        )

        elements.append(
            Spacer(1, 20)
        )

        # -------------------------------------------------
        # 会局・方合
        # -------------------------------------------------

        elements.append(
            Paragraph("【会局・方合】", style)
        )

        if report.combinations:

            elements.append(
                Paragraph(
                    f"会局：{report.combinations.kaikyoku or 'なし'}",
                    style,
                )
            )

            elements.append(
                Paragraph(
                    f"方合：{report.combinations.hogo or 'なし'}",
                    style,
                )
            )

        elements.append(
            Spacer(1, 20)
        )

        # -------------------------------------------------
        # 神殺・宮位
        # -------------------------------------------------

        if report.house_gods:

            elements.append(
                Paragraph("【神殺・宮位】", style)
            )

            for house in (
                report.house_gods.year,
                report.house_gods.month,
                report.house_gods.day,
                report.house_gods.hour,
            ):

                gods = "、".join(house.gods)

                elements.append(
                    Paragraph(
                        f"{house.house}：{gods}",
                        style,
                    )
                )

        elements.append(
            Spacer(1, 20)
        )

        # -------------------------------------------------
        # AI鑑定
        # -------------------------------------------------

        if report.ai_reading:

            elements.append(
                Paragraph("【AI総合鑑定】", style)
            )

            sections = [

                ("総評", report.ai_reading.summary),
                ("性格", report.ai_reading.personality),
                ("才能", report.ai_reading.talent),
                ("仕事運", report.ai_reading.work),
                ("恋愛・結婚運", report.ai_reading.love),
                ("健康運", report.ai_reading.health),
                ("運勢", report.ai_reading.fortune),
                ("アドバイス", report.ai_reading.advice),

            ]

            for title, text in sections:

                elements.append(
                    Paragraph(
                        f"【{title}】",
                        style,
                    )
                )

                elements.append(
                    Paragraph(
                        text,
                        style,
                    )
                )

                elements.append(
                    Spacer(1, 8)
                )

        # -------------------------------------------------
        # PDF生成
        # -------------------------------------------------

        doc.build(elements)