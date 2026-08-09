import unittest

from fortune_core.iching.hexagrams import HexagramEngine
from fortune_core.iching.interpretation_modules.rules import (
    interpret_double_line,
    interpret_five_lines,
    interpret_four_lines,
    interpret_no_change,
    interpret_single_line,
    interpret_six_lines,
    interpret_three_lines,
)


class TestInterpretationRules(unittest.TestCase):

    def setUp(self) -> None:
        self.hexagram_engine = HexagramEngine()

    def test_interpret_no_change(self) -> None:
        result = self.hexagram_engine.generate(
            [8, 8, 8, 8, 8, 8]
        )

        interpretation = interpret_no_change()

        self.assertEqual(
            interpretation.mode,
            "hexagram",
        )
        self.assertEqual(
            interpretation.title,
            "本卦",
        )
        self.assertEqual(
            interpretation.lines,
            [],
        )

    def test_interpret_single_line(self) -> None:
        result = self.hexagram_engine.generate(
            [9, 8, 8, 8, 8, 8]
        )

        interpretation = interpret_single_line(
            self.hexagram_engine,
            result,
        )

        self.assertEqual(
            interpretation.mode,
            "single_line",
        )
        self.assertEqual(
            interpretation.title,
            "初九",
        )
        self.assertEqual(
            len(interpretation.lines),
            1,
        )
        self.assertEqual(
            interpretation.lines[0].line,
            1,
        )

    def test_interpret_double_line(self) -> None:
        result = self.hexagram_engine.generate(
            [9, 9, 8, 8, 8, 8]
        )

        interpretation = interpret_double_line(
            self.hexagram_engine,
            result,
        )

        self.assertEqual(
            interpretation.mode,
            "double_line",
        )
        self.assertEqual(
            interpretation.title,
            "九二",
        )
        self.assertEqual(
            len(interpretation.lines),
            1,
        )
        self.assertEqual(
            interpretation.lines[0].line,
            2,
        )

    def test_interpret_three_lines(self) -> None:
        result = self.hexagram_engine.generate(
            [9, 9, 9, 8, 8, 8]
        )

        interpretation = interpret_three_lines(
            self.hexagram_engine,
            result,
        )

        self.assertEqual(
            interpretation.mode,
            "three_lines",
        )
        self.assertEqual(
            interpretation.title,
            "坤為地",
        )
        self.assertEqual(
            interpretation.lines,
            [],
        )

    def test_interpret_four_lines(self) -> None:
        result = self.hexagram_engine.generate(
            [9, 9, 9, 9, 8, 8]
        )

        interpretation = interpret_four_lines(
            self.hexagram_engine,
            result,
        )

        self.assertEqual(
            interpretation.mode,
            "four_lines",
        )
        self.assertEqual(
            interpretation.title,
            "坤為地",
        )
        self.assertEqual(
            len(interpretation.lines),
            2,
        )
        self.assertEqual(
            [line.line for line in interpretation.lines],
            [5, 6],
        )

    def test_interpret_five_lines(self) -> None:
        result = self.hexagram_engine.generate(
            [9, 9, 9, 9, 9, 8]
        )

        interpretation = interpret_five_lines(
            self.hexagram_engine,
            result,
        )

        self.assertEqual(
            interpretation.mode,
            "five_lines",
        )
        self.assertEqual(
            interpretation.title,
            "上六",
        )
        self.assertEqual(
            len(interpretation.lines),
            1,
        )
        self.assertEqual(
            interpretation.lines[0].line,
            6,
        )

    def test_interpret_six_lines(self) -> None:
        result = self.hexagram_engine.generate(
            [9, 9, 9, 9, 9, 9]
        )

        interpretation = interpret_six_lines(
            self.hexagram_engine,
            result,
        )

        self.assertEqual(
            interpretation.mode,
            "six_lines",
        )
        self.assertEqual(
            interpretation.title,
            "坤為地",
        )
        self.assertEqual(
            interpretation.lines,
            [],
        )


if __name__ == "__main__":
    unittest.main()
