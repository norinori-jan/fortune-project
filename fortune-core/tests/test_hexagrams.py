import unittest

from fortune_core.iching.hexagrams import HexagramEngine


class TestHexagramEngine(unittest.TestCase):

    def test_generate_qian(self) -> None:
        engine = HexagramEngine()

        result = engine.generate(
            [7, 7, 7, 7, 7, 7]
        )

        self.assertEqual(
            result.hexagram_number,
            1,
        )
        self.assertEqual(
            result.hexagram_name,
            "乾為天",
        )
        self.assertEqual(
            result.lower_trigram,
            "乾",
        )
        self.assertEqual(
            result.upper_trigram,
            "乾",
        )
        self.assertEqual(
            result.changing_lines,
            [],
        )

    def test_generate_with_one_changing_line(self) -> None:
        engine = HexagramEngine()

        result = engine.generate(
            [9, 7, 7, 7, 7, 7]
        )

        self.assertEqual(
            result.hexagram_number,
            1,
        )
        self.assertEqual(
            result.hexagram_name,
            "乾為天",
        )
        self.assertEqual(
            result.changing_lines,
            [1],
        )
        self.assertEqual(
            result.changed_hexagram_number,
            44,
        )
        self.assertEqual(
            result.changed_hexagram_name,
            "天風姤",
        )


if __name__ == "__main__":
    unittest.main()
