from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class FortuneResult:
    result_id: str
    system: str
    theme: str
    title: str
    summary: str
    message: str
    keywords: tuple[str, ...] = ()
    score: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "system": self.system,
            "theme": self.theme,
            "title": self.title,
            "summary": self.summary,
            "message": self.message,
            "keywords": list(self.keywords),
            "score": self.score,
            "metadata": dict(self.metadata),
        }