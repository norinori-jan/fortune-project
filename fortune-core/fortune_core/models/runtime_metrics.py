from __future__ import annotations
from dataclasses import dataclass
@dataclass(frozen=True)
class FortuneRuntimeMetrics:
    total_requests: int
    successful_requests: int
    failed_requests: int
    cache_hits: int
    cache_misses: int
    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return self.successful_requests / self.total_requests
    def to_dict(self) -> dict[str, float | int]:
        return {
            "total_requests": self.total_requests,
            "successful_requests": self.successful_requests,
            "failed_requests": self.failed_requests,
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "success_rate": self.success_rate,
        }