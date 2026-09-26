from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any
@dataclass(frozen=True)
class HubEvent:
    event_id: str
    event_type: str
    user_key: str
    operation: str
    theme: str
    timestamp: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    payload: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "event_id": self.event_id,
            "event_type": self.event_type,
            "user_key": self.user_key,
            "operation": self.operation,
            "theme": self.theme,
            "timestamp": self.timestamp,
            "payload": self.payload,
        }
