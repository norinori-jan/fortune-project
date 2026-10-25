from __future__ import annotations

import unittest

from fastapi import FastAPI
from fastapi.testclient import TestClient

from server.fortune_entry_api import router


class TestEntryAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        app = FastAPI()
        app.include_router(router)
        cls.client = TestClient(app)

    def test_entry_love(self) -> None:
        r = self.client.post("/fortune/entry", json={"question": "彼氏との結婚を迷っています"})
        self.assertEqual(r.status_code, 200)
        d = r.json()
        self.assertEqual(d["concern_type"], "love")
        self.assertEqual(d["recommended"]["tool"], "tarot")

    def test_entry_routes_to_each_tool(self) -> None:
        cases = {
            "生まれ持った性格を知りたい": "shichu",
            "この家の方角は？": "lopan",
            "転職するタイミングはいつ？": "iching",
            "彼の本音が知りたい": "tarot",
            "なんとなく不調": "tarot",
        }
        for q, tool in cases.items():
            r = self.client.post("/fortune/entry", json={"question": q}).json()
            self.assertEqual(r["recommended"]["tool"], tool, q)

    def test_entry_empty_is_rejected(self) -> None:
        r = self.client.post("/fortune/entry", json={"question": ""})
        self.assertEqual(r.status_code, 422)

    def test_celtic_cross_10_cards_and_seed_is_repeatable(self) -> None:
        body = {"question": "転職したい", "seed": 12345}
        a = self.client.post("/fortune/tarot/celtic", json=body).json()
        b = self.client.post("/fortune/tarot/celtic", json=body).json()
        self.assertEqual(a["spread"], "celtic_cross")
        self.assertEqual(len(a["positions"]), 10)
        self.assertEqual(a["positions"], b["positions"])

    def test_shichu_pillars_known_dates(self) -> None:
        # 2000-01-01 12:00 → 己卯年 丙子月 戊午日
        r = self.client.post("/fortune/shichu/pillars", json={"birth_date": "2000-01-01", "birth_time": "12:00"}).json()
        self.assertEqual([r["year"]["name"], r["month"]["name"], r["day"]["name"]], ["己卯", "丙子", "戊午"])
        # 立春（2024-02-04 17:27 JST）の前後で、年と月が切り替わる
        a = self.client.post("/fortune/shichu/pillars", json={"birth_date": "2024-02-04", "birth_time": "17:00"}).json()
        b = self.client.post("/fortune/shichu/pillars", json={"birth_date": "2024-02-04", "birth_time": "18:00"}).json()
        self.assertEqual((a["year"]["name"], a["month"]["name"]), ("癸卯", "乙丑"))
        self.assertEqual((b["year"]["name"], b["month"]["name"]), ("甲辰", "丙寅"))
        # 2024-01-01 は甲子日
        c = self.client.post("/fortune/shichu/pillars", json={"birth_date": "2024-01-01"}).json()
        self.assertEqual(c["day"]["name"], "甲子")
        self.assertNotIn("hour", c)

    def test_shichu_bad_date(self) -> None:
        r = self.client.post("/fortune/shichu/pillars", json={"birth_date": "2024/02/30"})
        self.assertEqual(r.status_code, 400)


if __name__ == "__main__":
    unittest.main()
