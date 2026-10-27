from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneRuntimeRecommendation:
    user_key: str
    theme: str
    system: str
    operation: str
    reason: str
    keywords: tuple[str, ...] = ()
    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "theme": self.theme,
            "system": self.system,
            "operation": self.operation,
            "reason": self.reason,
            "keywords": list(self.keywords),
        }
