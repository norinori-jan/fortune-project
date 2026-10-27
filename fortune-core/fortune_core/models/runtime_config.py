from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class FortuneRuntimeConfig:
    service_name: str = "fortune-hub"
    version: str = "1.0.0"
    default_theme: str = "general"
    default_operation: str = "home"
    cache_enabled: bool = True
    audit_enabled: bool = True
    event_enabled: bool = True
    max_requests_per_user: int = 60
    def to_dict(self) -> dict[str, object]:
        return {
            "service_name": self.service_name,
            "version": self.version,
            "default_theme": self.default_theme,
            "default_operation": self.default_operation,
            "cache_enabled": self.cache_enabled,
            "audit_enabled": self.audit_enabled,
            "event_enabled": self.event_enabled,
            "max_requests_per_user": self.max_requests_per_user,
        }
