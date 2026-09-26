from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class FortuneRuntimeContext:
    request_id: str
    user_key: str
    theme: str
    operation: str
    question: str = ""
    locale: str = "ja-JP"
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "user_key": self.user_key,
            "theme": self.theme,
            "operation": self.operation,
            "question": self.question,
            "locale": self.locale,
            "metadata": self.metadata,
        }