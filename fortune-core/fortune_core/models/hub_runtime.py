from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class HubRuntimeRequest:
    user_key: str
    question: str = ""
    theme: str = "general"
    operation: str = "home"
    use_cache: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)
@dataclass(frozen=True)
class HubRuntimeResponse:
    request_id: str
    operation: str
    user_key: str
    theme: str
    cached: bool
    result: dict[str, Any]
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "operation": self.operation,
            "user_key": self.user_key,
            "theme": self.theme,
            "cached": self.cached,
            "result": self.result,
            "metadata": self.metadata,
        }
