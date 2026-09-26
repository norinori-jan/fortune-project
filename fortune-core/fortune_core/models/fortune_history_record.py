from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneHistoryRecord:
    record_id: str
    question: str
    system: str
    title: str
    summary: str
    created_at: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.record_id,
            "question": self.question,
            "system": self.system,
            "title": self.title,
            "summary": self.summary,
            "created_at": self.created_at,
        }