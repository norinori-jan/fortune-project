from __future__ import annotations
from collections import defaultdict, deque
from threading import RLock
from time import monotonic
class FortuneRuntimeRateLimitError(Exception):
    pass
class FortuneRuntimeRateLimiter:
    def __init__(
        self,
        max_requests: int = 60,
        window_seconds: float = 60.0,
    ) -> None:
        self.max_requests = max(1, max_requests)
        self.window_seconds = max(1.0, window_seconds)
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = RLock()
    def allow(self, user_key: str) -> bool:
        now = monotonic()
        with self._lock:
            queue = self._requests[user_key]
            while queue and now - queue[0] >= self.window_seconds:
                queue.popleft()
            if len(queue) >= self.max_requests:
                return False
            queue.append(now)
            return True
    def require(self, user_key: str) -> None:
        if not self.allow(user_key):
            raise FortuneRuntimeRateLimitError(
                f"Rate limit exceeded for user: {user_key}"
            )
    def remaining(self, user_key: str) -> int:
        now = monotonic()
        with self._lock:
            queue = self._requests[user_key]
            while queue and now - queue[0] >= self.window_seconds:
                queue.popleft()
            return max(0, self.max_requests - len(queue))
