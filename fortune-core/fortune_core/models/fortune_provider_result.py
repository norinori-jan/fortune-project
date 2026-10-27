from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class FortuneProviderResult:
    provider: str
    system: str
    success: bool
    result: dict[str, Any]
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "provider": self.provider,
            "system": self.system,
            "success": self.success,
            "result": self.result,
            "error": self.error,
            "metadata": dict(self.metadata),
        }