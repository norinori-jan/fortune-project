from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChangingLineInterpretation:
    """
    変爻解釈
    """

    line: int
    position: str
    original: str
    translation: str
    meaning: str
    advice: str
    keywords: list[str]


@dataclass(frozen=True)
class Interpretation:
    """
    易経の解釈結果
    """

    mode: str
    title: str
    message: str
    lines: list[ChangingLineInterpretation]