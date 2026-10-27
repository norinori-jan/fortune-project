from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneResultReuse:
    source_id: str
    title: str
    question: str
    theme: str
    system: str
    result: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "title": self.title,
            "question": self.question,
            "theme": self.theme,
            "system": self.system,
            "result": self.result,
        }