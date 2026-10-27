from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class QuestionSuggestion:
    question: str
    theme: str
    system: str
    reason: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "theme": self.theme,
            "system": self.system,
            "reason": self.reason,
        }