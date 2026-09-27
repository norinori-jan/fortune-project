from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeBootstrap:
    service: str
    version: str
    user_key: str
    theme: str
    daily: dict[str, Any]
    profile: dict[str, Any]
    preferences: dict[str, Any]
    recommendations: tuple[dict[str, Any], ...]
    features: tuple[dict[str, Any], ...]
    contract: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "version": self.version,
            "user_key": self.user_key,
            "theme": self.theme,
            "daily": self.daily,
            "profile": self.profile,
            "preferences": self.preferences,
            "recommendations": list(self.recommendations),
            "features": list(self.features),
            "contract": self.contract,
        }