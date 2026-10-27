from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneResultScreen:
    result: dict[str, Any]
    card: dict[str, Any]
    share: dict[str, Any]
    actions: tuple[dict[str, Any], ...]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result": self.result,
            "card": self.card,
            "share": self.share,
            "actions": list(self.actions),
            "metadata": self.metadata,
        }