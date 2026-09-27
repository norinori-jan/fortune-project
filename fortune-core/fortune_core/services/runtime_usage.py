from __future__ import annotations

from threading import RLock

from fortune_core.models.runtime_usage import FortuneRuntimeUsage


class FortuneRuntimeUsageService:
    def __init__(self) -> None:
        self._usage: dict[str, FortuneRuntimeUsage] = {}
        self._lock = RLock()

    def record(
        self,
        user_key: str,
        *,
        success: bool,
        cached: bool = False,
    ) -> FortuneRuntimeUsage:
        with self._lock:
            current = self._usage.get(
                user_key,
                FortuneRuntimeUsage(user_key=user_key),
            )

            item = FortuneRuntimeUsage(
                user_key=user_key,
                requests=current.requests + 1,
                successful=(
                    current.successful + (1 if success else 0)
                ),
                failed=(
                    current.failed + (0 if success else 1)
                ),
                cached=(
                    current.cached + (1 if cached else 0)
                ),
            )

            self._usage[user_key] = item
            return item

    def get(self, user_key: str) -> FortuneRuntimeUsage:
        with self._lock:
            return self._usage.get(
                user_key,
                FortuneRuntimeUsage(user_key=user_key),
            )