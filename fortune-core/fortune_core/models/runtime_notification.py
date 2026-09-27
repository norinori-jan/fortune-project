from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FortuneRuntimeNotificationPreference:
    user_key: str
    enabled: bool = True
    morning: bool = True
    afternoon: bool = False
    evening: bool = True

    def to_dict(self) -> dict[str, object]:
        return {
            "user_key": self.user_key,
            "enabled": self.enabled,
            "morning": self.morning,
            "afternoon": self.afternoon,
            "evening": self.evening,
        }