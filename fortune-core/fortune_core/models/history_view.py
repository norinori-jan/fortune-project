from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneHistoryViewItem:
    request_id: str
    title: str
    theme: str
    operation: str
    question: str
    created_at: str
    result: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "title": self.title,
            "theme": self.theme,
            "operation": self.operation,
            "question": self.question,
            "created_at": self.created_at,
            "result": self.result,
        }