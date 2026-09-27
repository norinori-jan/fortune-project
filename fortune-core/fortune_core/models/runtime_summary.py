from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneRuntimeSummary:
    user_key: str
    total_requests: int
    successful_requests: int
    cached_requests: int
    themes: tuple[str, ...]
    operations: tuple[str, ...]
    latest_request_id: str | None
    latest_theme: str | None
    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "cached_requests": self.cached_requests,
            "themes": list(self.themes),
            "operations": list(self.operations),
            "latest_request_id": self.latest_request_id,
            "latest_theme": self.latest_theme,
        }