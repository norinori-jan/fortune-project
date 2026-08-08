from __future__ import annotations

from .changing_lines import normalize_line
from .models import Interpretation


def interpret_no_change() -> Interpretation:
    """
    変爻がない場合の解釈。
    """

    return Interpretation(
        mode="hexagram",
        title="本卦",
        message="変爻がありません。本卦の卦辞・象伝を読みます。",
        lines=[],
    )


def interpret_single_line(
    hexagram_engine,
    result,
) -> Interpretation:
    """
    変爻が1本の場合の解釈。
    """

    target = result.changing_lines[0]

    raw_line = hexagram_engine.get_line(
        result,
        target,
    )

    line = normalize_line(
        target,
        raw_line,
    )

    return Interpretation(
        mode="single_line",
        title=line.position,
        message="変爻が1本です。この爻辞を中心に読みます。",
        lines=[line],
    )


def interpret_double_line(
    hexagram_engine,
    result,
) -> Interpretation:
    """
    変爻が2本の場合の解釈。

    上位の変爻を読む。
    """

    target = max(result.changing_lines)

    raw_line = hexagram_engine.get_line(
        result,
        target,
    )

    line = normalize_line(
        target,
        raw_line,
    )

    return Interpretation(
        mode="double_line",
        title=line.position,
        message="変爻が2本です。上位の変爻を読みます。",
        lines=[line],
    )


def interpret_three_lines(
    hexagram_engine,
    result,
) -> Interpretation:
    """
    変爻が3本の場合の解釈。
    """

    changed = hexagram_engine.get_changed_hexagram(
        result
    )

    return Interpretation(
        mode="three_lines",
        title=changed.get(
            "name",
            "",
        ),
        message="変爻が3本です。本卦と変卦の両方を参考にします。",
        lines=[],
    )


def interpret_four_lines(
    hexagram_engine,
    result,
) -> Interpretation:
    """
    変爻が4本の場合の解釈。

    変卦の変わらない二爻を読む。
    """

    changed = hexagram_engine.get_changed_hexagram(
        result
    )

    unchanged = [
        i
        for i in range(1, 7)
        if i not in result.changing_lines
    ]

    lines = [
        normalize_line(
            i,
            changed["yao"]["lines"][str(i)],
        )
        for i in unchanged
    ]

    return Interpretation(
        mode="four_lines",
        title=changed.get(
            "name",
            "",
        ),
        message="変卦の変わらない二爻を読みます。",
        lines=lines,
    )


def interpret_five_lines(
    hexagram_engine,
    result,
) -> Interpretation:
    """
    変爻が5本の場合の解釈。

    変卦の変わらない一爻を読む。
    """

    changed = hexagram_engine.get_changed_hexagram(
        result
    )

    unchanged = [
        i
        for i in range(1, 7)
        if i not in result.changing_lines
    ][0]

    raw_line = changed["yao"]["lines"][str(unchanged)]

    line = normalize_line(
        unchanged,
        raw_line,
    )

    return Interpretation(
        mode="five_lines",
        title=line.position,
        message="変卦の変わらない一爻を読みます。",
        lines=[line],
    )


def interpret_six_lines(
    hexagram_engine,
    result,
) -> Interpretation:
    """
    変爻が6本の場合の解釈。
    """

    changed = hexagram_engine.get_changed_hexagram(
        result
    )

    return Interpretation(
        mode="six_lines",
        title=changed.get(
            "name",
            "",
        ),
        message="全ての爻が変化しました。変卦を中心に読みます。",
        lines=[],
    )


__all__ = [
    "interpret_no_change",
    "interpret_single_line",
    "interpret_double_line",
    "interpret_three_lines",
    "interpret_four_lines",
    "interpret_five_lines",
    "interpret_six_lines",
]