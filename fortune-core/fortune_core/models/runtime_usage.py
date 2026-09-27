from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FortuneRuntimeUsage:
    user_key: str
    requests: int = 0
    successful: int = 0
    failed: int = 0
    cached: int = 0

    @property
    def success_rate(self) -> float:
        if self.requests == 0:
            return 0.0
        return round(self.successful / self.requests, 4)

    def to_dict(self) -> dict[str, object]:
        return {
            "user_key": self.user_key,
            "requests": self.requests,
            "successful": self.successful,
            "failed": self.failed,
            "cached": self.cached,
            "success_rate": self.success_rate,
        }