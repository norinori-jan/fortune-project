from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any
@dataclass(frozen=True, slots=True)
class FortuneHistoryItem:
    id: str
    created_at: datetime
    system: str
    question: str
    result: dict[str, Any]
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "created_at": self.created_at.isoformat(),
            "system": self.system,
            "question": self.question,
            "result": self.result,
        }