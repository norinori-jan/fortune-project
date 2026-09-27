from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeHistoryItem:
    request_id: str
    user_key: str
    operation: str
    theme: str
    question: str
    result: dict[str, Any]
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "user_key": self.user_key,
            "operation": self.operation,
            "theme": self.theme,
            "question": self.question,
            "result": self.result,
            "created_at": self.created_at,
        }