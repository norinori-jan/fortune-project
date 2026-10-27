from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimePlatformSnapshot:
    service: str
    version: str
    user_key: str
    preferences: dict[str, Any]
    usage: dict[str, Any]
    notifications: dict[str, Any]
    features: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "version": self.version,
            "user_key": self.user_key,
            "preferences": self.preferences,
            "usage": self.usage,
            "notifications": self.notifications,
            "features": list(self.features),
        }