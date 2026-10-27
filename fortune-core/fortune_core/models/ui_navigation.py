from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneUiNavigationItem:
    key: str
    label: str
    path: str
    icon: str
    active: bool = False
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "label": self.label,
            "path": self.path,
            "icon": self.icon,
            "active": self.active,
            "metadata": self.metadata or {},
        }