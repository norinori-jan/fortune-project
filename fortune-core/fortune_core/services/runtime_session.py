from __future__ import annotations
from dataclasses import dataclass, field
from threading import RLock
from typing import Any
@dataclass
class FortuneRuntimeSession:
    session_id: str
    user_key: str
    request_ids: list[str] = field(default_factory=list)
    last_request_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "user_key": self.user_key,
            "request_ids": list(self.request_ids),
            "last_request_id": self.last_request_id,
            "metadata": dict(self.metadata),
        }
class FortuneRuntimeSessionService:
    def __init__(self, max_requests: int = 100) -> None:
        self.max_requests = max(1, max_requests)
        self._sessions: dict[str, FortuneRuntimeSession] = {}
        self._lock = RLock()
    def get_or_create(
        self,
        session_id: str,
        user_key: str,
    ) -> FortuneRuntimeSession:
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                session = FortuneRuntimeSession(
                    session_id=session_id,
                    user_key=user_key,
                )
                self._sessions[session_id] = session
            return session
    def record(
        self,
        session_id: str,
        request_id: str,
        user_key: str,
    ) -> FortuneRuntimeSession:
        session = self.get_or_create(session_id, user_key)
        with self._lock:
            session.request_ids.append(request_id)
            session.last_request_id = request_id
            if len(session.request_ids) > self.max_requests:
                session.request_ids = session.request_ids[
                    -self.max_requests:
                ]
            return session
    def get(
        self,
        session_id: str,
    ) -> FortuneRuntimeSession | None:
        with self._lock:
            return self._sessions.get(session_id)
    def list(self) -> list[FortuneRuntimeSession]:
        with self._lock:
            return list(self._sessions.values())
