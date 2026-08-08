from __future__ import annotations

from .hexagrams import (
    HexagramEngine,
    HexagramResult,
)

from .interpretation_modules.models import (
    Interpretation,
)

from .interpretation_modules.rules import (
    interpret_double_line,
    interpret_five_lines,
    interpret_four_lines,
    interpret_no_change,
    interpret_single_line,
    interpret_six_lines,
    interpret_three_lines,
)


class InterpretationEngine:
    """
    易経 解釈エンジン

    HexagramEngine が生成した HexagramResult を元に、
    易占のルールに従って
    「どの卦・どの爻を読むべきか」
    を決定する。

    実際の解釈ルールは
    interpretation_modules/rules.py
    に分離する。
    """

    def __init__(self) -> None:

        self.hexagram_engine = HexagramEngine()

    # ---------------------------------------------------------
    # 解釈
    # ---------------------------------------------------------

    def interpret(
        self,
        result: HexagramResult,
    ) -> Interpretation:
        """
        HexagramResult を解釈する。

        変爻の本数に応じて、
        interpretation_modules.rules
        の対応するルールを呼び出す。
        """

        count = len(
            result.changing_lines
        )

        # ---------------------------------------------
        # 変爻なし
        # ---------------------------------------------

        if count == 0:

            return interpret_no_change()

        # ---------------------------------------------
        # 一変
        # ---------------------------------------------

        if count == 1:

            return interpret_single_line(
                self.hexagram_engine,
                result,
            )

        # ---------------------------------------------
        # 二変
        # ---------------------------------------------

        if count == 2:

            return interpret_double_line(
                self.hexagram_engine,
                result,
            )

        # ---------------------------------------------
        # 三変
        # ---------------------------------------------

        if count == 3:

            return interpret_three_lines(
                self.hexagram_engine,
                result,
            )

        # ---------------------------------------------
        # 四変
        # ---------------------------------------------

        if count == 4:

            return interpret_four_lines(
                self.hexagram_engine,
                result,
            )

        # ---------------------------------------------
        # 五変
        # ---------------------------------------------

        if count == 5:

            return interpret_five_lines(
                self.hexagram_engine,
                result,
            )

        # ---------------------------------------------
        # 六変
        # ---------------------------------------------

        return interpret_six_lines(
            self.hexagram_engine,
            result,
        )


__all__ = [
    "InterpretationEngine",
]

