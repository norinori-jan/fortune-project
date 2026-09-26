from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneResponseMeta:
    api_version: str
    service: str
    request_id: str
    theme: str
    system_count: int
    generated_at: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "api_version": self.api_version,
            "service": self.service,
            "request_id": self.request_id,
            "theme": self.theme,
            "system_count": self.system_count,
            "generated_at": self.generated_at,
        }