from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True, slots=True)
class FortunePlatformSettings:
    service_name: str = "fortune-platform"
    api_version: str = "3.0.0"
    default_provider: str = "complete"
    history_enabled: bool = True
    max_history_items: int = 100