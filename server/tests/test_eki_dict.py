from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from fortune_core.iching import eki_dict
from server.main import app


class TestEkiDict(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_all_64_hexagrams_loaded(self) -> None:
        for n in range(1, 65):
            entry = eki_dict.hexagram_entry(n)
            self.assertIsNotNone(entry, n)
            self.assertIsNotNone(entry["meaning"], n)

    def test_classify(self) -> None:
        self.assertEqual(eki_dict.classify_question("転職しても良いですか？"), "仕事・就職・昇進はどう？")
        self.assertIsNone(eki_dict.classify_question("ぼんやりした気分"))

    def test_reading_unknown_type_returns_meaning_only(self) -> None:
        r = eki_dict.eki_reading(1, question_text="ぼんやりした気分")
        self.assertIsNone(r["question_type"])
        self.assertEqual(len(r["main"]["topics"]), len(eki_dict.hexagram_entry(1)["topics"]))

    def test_reading_with_change(self) -> None:
        r = eki_dict.eki_reading(8, 23, [5], "お金は入りますか")
        self.assertEqual(r["main"]["name"], "水地比")
        self.assertEqual(r["changed"]["name"], "山地剥")
        self.assertLessEqual(len(r["main"]["topics"]), 1)

    def test_endpoints(self) -> None:
        r = self.client.get("/eki/dict/8", params={"question": "勝てる？"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["name"], "水地比")
        self.assertEqual(self.client.get("/eki/dict/99").status_code, 404)
        self.assertGreater(self.client.get("/eki/dict", params={"word": "争い"}).json()["count"], 0)
        r = self.client.post("/iching/eki", json={"question": "転職しても良いですか？"})
        self.assertEqual(r.status_code, 200)
        self.assertIn("eki", r.json())


if __name__ == "__main__":
    unittest.main()
