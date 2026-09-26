from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneNotification:
    notification_id: str
    title: str
    message: str
    category: str
    timing: str
    enabled: bool = True
    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.notification_id,
            "title": self.title,
            "message": self.message,
            "category": self.category,
            "timing": self.timing,
            "enabled": self.enabled,
        }