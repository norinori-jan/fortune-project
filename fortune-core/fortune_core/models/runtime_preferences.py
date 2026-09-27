from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimePreferences:
    user_key: str
    theme: str = "general"
    language: str = "ja"
    notifications_enabled: bool = True
    daily_enabled: bool = True
    favorite_systems: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "theme": self.theme,
            "language": self.language,
            "notifications_enabled": self.notifications_enabled,
            "daily_enabled": self.daily_enabled,
            "favorite_systems": list(self.favorite_systems),
            "metadata": self.metadata,
        }