from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeDashboard:
    user_key: str
    theme: str
    daily: dict[str, Any]
    profile: dict[str, Any]
    summary: dict[str, Any]
    recommendations: tuple[dict[str, Any], ...]
    favorites: tuple[dict[str, Any], ...]
    recent_history: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "theme": self.theme,
            "daily": self.daily,
            "profile": self.profile,
            "summary": self.summary,
            "recommendations": list(self.recommendations),
            "favorites": list(self.favorites),
            "recent_history": list(self.recent_history),
        }