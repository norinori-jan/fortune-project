from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from typing import Any
@dataclass(frozen=True)
class FortuneRunRecord:
    execution_id: str
    theme: str
    question: str
    created_at: datetime
    systems: tuple[str, ...]
    result_count: int
    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "theme": self.theme,
            "question": self.question,
            "created_at": self.created_at.isoformat(),
            "systems": list(self.systems),
            "result_count": self.result_count,
        }
