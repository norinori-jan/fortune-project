from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class FortuneHubWidget:
    key: str
    title: str
    widget_type: str
    priority: int
    data: dict[str, Any] = field(default_factory=dict)
    actions: tuple[str, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "widget_type": self.widget_type,
            "priority": self.priority,
            "data": self.data,
            "actions": list(self.actions),
        }