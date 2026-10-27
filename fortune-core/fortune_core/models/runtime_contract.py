from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeContract:
    name: str
    version: str
    operations: tuple[str, ...]
    themes: tuple[str, ...]
    systems: tuple[str, ...]
    features: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "version": self.version,
            "operations": list(self.operations),
            "themes": list(self.themes),
            "systems": list(self.systems),
            "features": list(self.features),
        }