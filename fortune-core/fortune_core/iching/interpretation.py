from __future__ import annotations

from dataclasses import dataclass

from .hexagrams import HexagramEngine, HexagramResult


@dataclass(frozen=True)
class Interpretation:
    """
    易経の解釈結果
    """

    mode: str

    title: str

    message: str

    lines: list[dict]


class InterpretationEngine:
    """
    易経 解釈エンジン

    HexagramEngine が生成した HexagramResult を元に、
    易占のルールに従って
    「どの卦・どの爻を読むべきか」
    を決定する。
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

        count = len(result.changing_lines)

        # ---------------------------------------------
        # 変爻なし
        # ---------------------------------------------

        if count == 0:

            return Interpretation(

                mode="hexagram",

                title="本卦",

                message="変爻がありません。本卦の卦辞・象伝を読みます。",

                lines=[],
            )

        # ---------------------------------------------
        # 一変
        # ---------------------------------------------

        if count == 1:

            line = self.hexagram_engine.get_line(
                result,
                result.changing_lines[0],
            )

            return Interpretation(

                mode="single_line",

                title=line.get(
                    "position",
                    "",
                ),

                message="変爻が1本です。この爻辞を中心に読みます。",

                lines=[line],
            )

        # ---------------------------------------------
        # 二変
        # ---------------------------------------------

        if count == 2:

            target = max(result.changing_lines)

            line = self.hexagram_engine.get_line(
                result,
                target,
            )

            return Interpretation(

                mode="double_line",

                title=line.get(
                    "position",
                    "",
                ),

                message="変爻が2本です。上位の変爻を読みます。",

                lines=[line],
            )

        # ---------------------------------------------
        # 三変
        # ---------------------------------------------

        if count == 3:

            changed = self.hexagram_engine.get_changed_hexagram(
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

        # ---------------------------------------------
        # 四変
        # ---------------------------------------------

        if count == 4:

            changed = self.hexagram_engine.get_changed_hexagram(
                result
            )

            unchanged = [

                i

                for i in range(1, 7)

                if i not in result.changing_lines

            ]

            lines = [

                changed["yao"]["lines"][str(i)]

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

        # ---------------------------------------------
        # 五変
        # ---------------------------------------------

        if count == 5:

            changed = self.hexagram_engine.get_changed_hexagram(
                result
            )

            unchanged = [

                i

                for i in range(1, 7)

                if i not in result.changing_lines

            ][0]

            line = changed["yao"]["lines"][str(unchanged)]

            return Interpretation(

                mode="five_lines",

                title=line.get(
                    "position",
                    "",
                ),

                message="変卦の変わらない一爻を読みます。",

                lines=[line],
            )

        # ---------------------------------------------
        # 六変
        # ---------------------------------------------

        changed = self.hexagram_engine.get_changed_hexagram(
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