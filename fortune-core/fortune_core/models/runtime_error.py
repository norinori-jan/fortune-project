from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneRuntimeError:
    code: str
    message: str
    operation: str = ""
    request_id: str | None = None
    details: dict[str, Any] | None = None
    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "message": self.message,
            "operation": self.operation,
            "request_id": self.request_id,
            "details": self.details or {},
        }
