from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeExport:
    user_key: str
    generated_at: str
    profile: dict[str, Any]
    summary: dict[str, Any]
    preferences: dict[str, Any]
    usage: dict[str, Any]
    notifications: dict[str, Any]
    recommendations: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "generated_at": self.generated_at,
            "profile": self.profile,
            "summary": self.summary,
            "preferences": self.preferences,
            "usage": self.usage,
            "notifications": self.notifications,
            "recommendations": list(self.recommendations),
        }