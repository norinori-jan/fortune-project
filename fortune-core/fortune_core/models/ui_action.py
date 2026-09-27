from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneUiAction:
    key: str
    label: str
    action_type: str
    target: str
    payload: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "label": self.label,
            "action_type": self.action_type,
            "target": self.target,
            "payload": self.payload,
        }