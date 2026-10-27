from __future__ import annotations
import hashlib
from threading import RLock
from fortune_core.models.fortune_session import FortuneSession
class FortuneSessionService:
    def __init__(self) -> None:
        self._sessions: dict[str, FortuneSession] = {}
        self._lock = RLock()
    @staticmethod
    def _make_id(
        question: str,
        system: str,
        theme: str,
    ) -> str:
        raw = f"{question}|{system}|{theme}"
        return hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:20]
    def create(
        self,
        question: str,
        system: str = "unified",
        theme: str = "general",
    ) -> FortuneSession:
        session_id = self._make_id(
            question,
            system,
            theme,
        )
        session = FortuneSession(
            session_id=session_id,
            question=question,
            system=system,
            theme=theme,
        )
        with self._lock:
            self._sessions[session_id] = session
        return session
    def get(self, session_id: str) -> FortuneSession | None:
        with self._lock:
            return self._sessions.get(session_id)
    def list(self) -> tuple[FortuneSession, ...]:
        with self._lock:
            return tuple(self._sessions.values())
    def delete(self, session_id: str) -> bool:
        with self._lock:
            return self._sessions.pop(session_id, None) is not None