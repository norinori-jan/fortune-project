from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FortuneRuntimeFeature:
    name: str
    enabled: bool
    description: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "name": self.name,
            "enabled": self.enabled,
            "description": self.description,
        }
