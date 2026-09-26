from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneRuntimeAudit:
    audit_id: str
    request_id: str
    event_type: str
    operation: str
    user_key: str
    success: bool
    details: dict[str, Any]
    def to_dict(self) -> dict[str, Any]:
        return {
            "audit_id": self.audit_id,
            "request_id": self.request_id,
            "event_type": self.event_type,
            "operation": self.operation,
            "user_key": self.user_key,
            "success": self.success,
            "details": self.details,
        }