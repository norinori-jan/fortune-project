from __future__ import annotations

import unittest

from fastapi.testclient import TestClient

from server.main import app


class TestServerAPI(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = TestClient(app)

    def test_root(self) -> None:
        response = self.client.get("/")

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(
            data["service"],
            "fortune-project",
        )

        self.assertEqual(
            data["engine"],
            "I Ching",
        )

        self.assertEqual(
            data["status"],
            "ok",
        )

    def test_health(self) -> None:
        response = self.client.get("/health")

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(
            data["status"],
            "ok",
        )

        self.assertEqual(
            data["service"],
            "fortune-api",
        )

        self.assertTrue(
            data["modules"]["iching"],
        )

    def test_methods(self) -> None:
        response = self.client.get("/methods")

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(
            data["methods"],
            [
                "coin",
                "simple_yarrow",
                "traditional_yarrow",
            ],
        )

    def test_iching(self) -> None:
        response = self.client.post(
            "/iching",
            json={
                "question": "テスト質問",
                "method": "coin",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(
            data["question"],
            "テスト質問",
        )

        self.assertEqual(
            data["method"],
            "coin",
        )

        self.assertIn(
            "hexagram",
            data,
        )

        self.assertIn(
            "interpretation",
            data,
        )

    def test_iching_v2_without_changing_lines(self) -> None:
        response = self.client.post(
            "/iching/v2",
            json={
                "question": "テスト質問",
                "method": "coin",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        self.assertEqual(
            data["question"],
            "テスト質問",
        )

        self.assertEqual(
            data["method"],
            "coin",
        )

        self.assertIn(
            "primary",
            data,
        )

        self.assertIn(
            "changing_lines",
            data,
        )

        self.assertIn(
            "changed",
            data,
        )

        self.assertIn(
            "interpretation",
            data,
        )

        self.assertIsInstance(
            data["primary"],
            dict,
        )

        self.assertIsInstance(
            data["changing_lines"],
            list,
        )

    def test_iching_v2_response_structure(self) -> None:
        response = self.client.post(
            "/iching/v2",
            json={
                "question": "転職しても良いですか？",
                "method": "coin",
            },
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        data = response.json()

        primary = data["primary"]

        self.assertIn(
            "number",
            primary,
        )

        self.assertIn(
            "name",
            primary,
        )

        self.assertIn(
            "upper",
            primary,
        )

        self.assertIn(
            "lower",
            primary,
        )

        self.assertIn(
            "judgement",
            primary,
        )

        self.assertIn(
            "image",
            primary,
        )

        interpretation = data["interpretation"]

        self.assertIn(
            "mode",
            interpretation,
        )

        self.assertIn(
            "title",
            interpretation,
        )

        self.assertIn(
            "message",
            interpretation,
        )

        self.assertIn(
            "lines",
            interpretation,
        )


if __name__ == "__main__":
    unittest.main()
