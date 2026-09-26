from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneApiMeta:
    service: str = "fortune-platform"
    version: str = "2"
    deterministic: bool = True
    def to_dict(self) -> dict[str, Any]:
        return {
            "service": self.service,
            "version": self.version,
            "deterministic": self.deterministic,
        }
