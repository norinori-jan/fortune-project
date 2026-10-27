from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneRuntimeHealth:
    status: str
    service: str
    version: str
    checks: dict[str, bool]
    metrics: dict[str, Any]
    def to_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "service": self.service,
            "version": self.version,
            "checks": self.checks,
            "metrics": self.metrics,
        }

