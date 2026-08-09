import unittest

from fortune_core.iching import (
    FortuneEngine,
    FortuneResult,
)


class TestFortuneEngine(unittest.TestCase):

    def test_available_methods(self) -> None:
        engine = FortuneEngine()

        self.assertEqual(
            engine.available_methods(),
            [
                "coin",
                "simple_yarrow",
                "traditional_yarrow",
            ],
        )

    def test_from_numbers_without_changing_lines(self) -> None:
        engine = FortuneEngine()

        result = engine.from_numbers(
            [8, 8, 8, 8, 8, 8]
        )

        self.assertIsInstance(
            result,
            FortuneResult,
        )

        self.assertEqual(
            result.hexagram.hexagram_number,
            2,
        )

        self.assertEqual(
            result.hexagram.hexagram_name,
            "坤為地",
        )

        self.assertEqual(
            result.hexagram.changing_lines,
            [],
        )

        self.assertEqual(
            result.interpretation.mode,
            "hexagram",
        )

        self.assertEqual(
            result.interpretation.title,
            "本卦",
        )

    def test_from_numbers_with_one_changing_line(self) -> None:
        engine = FortuneEngine()

        result = engine.from_numbers(
            [9, 8, 8, 8, 8, 8]
        )

        self.assertEqual(
            result.hexagram.hexagram_number,
            24,
        )

        self.assertEqual(
            result.hexagram.hexagram_name,
            "地雷復",
        )

        self.assertEqual(
            result.hexagram.changing_lines,
            [1],
        )

        self.assertEqual(
            result.interpretation.mode,
            "single_line",
        )

        self.assertEqual(
            result.interpretation.title,
            "初九",
        )

        self.assertEqual(
            len(result.interpretation.lines),
            1,
        )

    def test_divine_by_coin(self) -> None:
        engine = FortuneEngine()

        result = engine.divine_by_coin(
            "テスト質問"
        )

        self.assertIsInstance(
            result,
            FortuneResult,
        )

        self.assertEqual(
            result.question,
            "テスト質問",
        )

        self.assertEqual(
            result.method,
            "coin",
        )

        self.assertIsNotNone(
            result.hexagram,
        )

        self.assertIsNotNone(
            result.interpretation,
        )

    def test_unknown_method(self) -> None:
        engine = FortuneEngine()

        with self.assertRaises(ValueError):
            engine.divine(
                "テスト質問",
                method="unknown",
            )


if __name__ == "__main__":
    unittest.main()
