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
        self.assertIn("recommendation", d)

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


if __name__ == "__main__":
    unittest.main()
