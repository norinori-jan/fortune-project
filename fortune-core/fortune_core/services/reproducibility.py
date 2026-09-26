from __future__ import annotations
import hashlib
import json
from typing import Any
class FortuneReproducibilityService:
    @staticmethod
    def make_key(
        system: str,
        question: str,
        options: dict[str, Any] | None = None,
    ) -> str:
        payload = {
            "system": system,
            "question": question,
            "options": options or {},
        }
        encoded = json.dumps(
            payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(
            encoded.encode("utf-8")
        ).hexdigest()
    @staticmethod
    def short_key(full_key: str) -> str:
        return full_key[:16]
