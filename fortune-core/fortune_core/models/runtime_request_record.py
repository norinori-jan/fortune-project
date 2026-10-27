from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class FortuneRuntimeRequestRecord:
    request_id: str
    user_key: str
    operation: str
    theme: str
    success: bool
    cached: bool
    result: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "user_key": self.user_key,
            "operation": self.operation,
            "theme": self.theme,
            "success": self.success,
            "cached": self.cached,
            "result": self.result,
        }