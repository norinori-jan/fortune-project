from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneApiEnvelope:
    ok: bool
    meta: dict[str, Any]
    data: Any
    errors: tuple[str, ...] = ()
    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "meta": self.meta,
            "data": self.data,
            "errors": list(self.errors),
        }
