from __future__ import annotations
from threading import RLock
from typing import Any
from fortune_core.models.runtime_user_state import FortuneRuntimeUserState
class FortuneRuntimeUserStateService:
    def __init__(self, max_recent: int = 50) -> None:
        self.max_recent = max(1, max_recent)
        self._states: dict[str, FortuneRuntimeUserState] = {}
        self._lock = RLock()
    def get(self, user_key: str) -> FortuneRuntimeUserState:
        with self._lock:
            return self._states.get(
                user_key,
                FortuneRuntimeUserState(user_key=user_key),
            )
    def update(
        self,
        user_key: str,
        *,
        session_id: str | None = None,
        theme: str | None = None,
        request_id: str | None = None,
        favorite_ids: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> FortuneRuntimeUserState:
        with self._lock:
            current = self.get(user_key)
            recent = list(current.recent_request_ids)
            if request_id:
                recent.append(request_id)
                recent = recent[-self.max_recent:]
            favorites = (
                tuple(favorite_ids)
                if favorite_ids is not None
                else current.favorite_ids
            )
            state = FortuneRuntimeUserState(
                user_key=user_key,
                session_id=(
                    session_id
                    if session_id is not None
                    else current.session_id
                ),
                theme=(
                    theme
                    if theme is not None
                    else current.theme
                ),
                last_request_id=(
                    request_id
                    if request_id is not None
                    else current.last_request_id
                ),
                favorite_ids=favorites,
                recent_request_ids=tuple(recent),
                metadata={
                    **current.metadata,
                    **(metadata or {}),
                },
            )
            self._states[user_key] = state
            return state
