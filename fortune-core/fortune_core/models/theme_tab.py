from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FortuneThemeTab:
    key: str
    label: str
    description: str
    active: bool = False

    def to_dict(self) -> dict:
        return {
            "key": self.key,
            "label": self.label,
            "description": self.description,
            "active": self.active,
        }
    