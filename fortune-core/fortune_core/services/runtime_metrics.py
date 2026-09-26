from __future__ import annotations
from threading import RLock
from fortune_core.models.runtime_metrics import FortuneRuntimeMetrics
class FortuneRuntimeMetricsService:
    def __init__(self) -> None:
        self._total = 0
        self._success = 0
        self._failed = 0
        self._cache_hits = 0
        self._cache_misses = 0
        self._lock = RLock()
    def request_started(self) -> None:
        with self._lock:
            self._total += 1
    def request_succeeded(self) -> None:
        with self._lock:
            self._success += 1
    def request_failed(self) -> None:
        with self._lock:
            self._failed += 1
    def cache_hit(self) -> None:
        with self._lock:
            self._cache_hits += 1
    def cache_miss(self) -> None:
        with self._lock:
            self._cache_misses += 1
    def snapshot(self) -> FortuneRuntimeMetrics:
        with self._lock:
            return FortuneRuntimeMetrics(
                total_requests=self._total,
                successful_requests=self._success,
                failed_requests=self._failed,
                cache_hits=self._cache_hits,
                cache_misses=self._cache_misses,
            )
    def reset(self) -> None:
        with self._lock:
            self._total = 0
            self._success = 0
            self._failed = 0
            self._cache_hits = 0
            self._cache_misses = 0