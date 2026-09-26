from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneScore:
    system: str
    theme: str
    score: int
    label: str
    reason: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "system": self.system,
            "theme": self.theme,
            "score": self.score,
            "label": self.label,
            "reason": self.reason,
        }
