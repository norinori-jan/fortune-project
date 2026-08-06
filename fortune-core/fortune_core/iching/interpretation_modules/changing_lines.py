from __future__ import annotations

from .models import ChangingLineInterpretation


def normalize_line(
    line_no: int,
    data: dict,
) -> ChangingLineInterpretation:
    """
    爻データを ChangingLineInterpretation に変換する。
    """

    return ChangingLineInterpretation(
        line=line_no,
        position=data.get(
            "position",
            "",
        ),
        original=data.get(
            "text",
            data.get(
                "original",
                "",
            ),
        ),
        translation=data.get(
            "translation",
            "",
        ),
        meaning=data.get(
            "meaning",
            "",
        ),
        advice=data.get(
            "advice",
            "",
        ),
        keywords=data.get(
            "keywords",
            [],
        ),
    )