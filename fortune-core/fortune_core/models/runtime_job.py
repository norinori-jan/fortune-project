from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class FortuneRuntimeJob:
    job_id: str
    operation: str
    user_key: str
    theme: str
    question: str = ""
    status: str = "queued"
    result: dict[str, Any] | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "job_id": self.job_id,
            "operation": self.operation,
            "user_key": self.user_key,
            "theme": self.theme,
            "question": self.question,
            "status": self.status,
            "result": self.result,
            "error": self.error,
            "metadata": self.metadata,
        }
