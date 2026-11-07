from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path

from fortune_core import ninso_library as n


class TestNinsoNorm(unittest.TestCase):

    def test_norm(self) -> None:
        self.assertEqual(n.norm("觀相 體質"), "観相体質")

    def test_search_old_kanji(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            doc = {"title": "第2輯", "pages": [{"seq": 1}],
                   "sections": [{"title": "由字面", "text": "此の人は氣力あり體格よし", "start_seq": 1}]}
            Path(d, "dai02.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
            os.environ["NINSO_PRIVATE_DIR"] = d
            try:
                self.assertEqual(len(n.search("気力")), 1)
                self.assertEqual(len(n.search("體格")), 1)
                self.assertIn("第 2巻", n.report())
            finally:
                del os.environ["NINSO_PRIVATE_DIR"]

    def test_rank_excerpt_alias(self) -> None:
        with tempfile.TemporaryDirectory() as d:
            secs = [{"title": "p1", "text": "眼は一度。", "start_seq": 1},
                    {"title": "p2", "text": "目の話。目は心の窓。目が大切。営養質あり", "start_seq": 2}]
            doc = {"title": "x", "pages": [{"seq": 1}, {"seq": 2}], "sections": secs}
            Path(d, "dai03.json").write_text(json.dumps(doc, ensure_ascii=False), encoding="utf-8")
            os.environ["NINSO_PRIVATE_DIR"] = d
            try:
                r = n.search("目")
                self.assertEqual(r[0]["title"], "p2")
                self.assertEqual(r[0]["count"], 3)
                self.assertIn("目", r[0]["excerpt"])
                self.assertEqual(len(n.lookup_type("me")["sections"]), 2)  # 目 + 眼
                self.assertEqual(len(n.search("栄養質")), 1)
            finally:
                del os.environ["NINSO_PRIVATE_DIR"]


if __name__ == "__main__":
    unittest.main()
