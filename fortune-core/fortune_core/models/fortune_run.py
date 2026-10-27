from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneRunRequest:
    question: str = ""
    theme: str = "general"
    user_key: str | None = None
    birth_date: str | None = None
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "theme": self.theme,
            "user_key": self.user_key,
            "birth_date": self.birth_date,
        }
@dataclass(frozen=True)
class FortuneRunResponse:
    execution_id: str
    result: dict[str, Any]
    def to_dict(self) -> dict[str, Any]:
        return {
            "execution_id": self.execution_id,
            "result": self.result,
        }