from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeOverview:
    contract: dict[str, Any]
    discovery: tuple[dict[str, Any], ...]
    help_items: tuple[dict[str, Any], ...]
    features: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract": self.contract,
            "discovery": list(self.discovery),
            "help": list(self.help_items),
            "features": list(self.features),
        }