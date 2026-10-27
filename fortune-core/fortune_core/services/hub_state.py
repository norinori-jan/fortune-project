from __future__ import annotations
from threading import RLock
from ..models.hub_state import FortuneHubState
class FortuneHubStateService:
    """
    永続DBに依存しないHub状態管理。
    後からDB/Redis等へ差し替えられる境界として使用する。
    """
    def __init__(self) -> None:
        self._states: dict[str, FortuneHubState] = {}
        self._lock = RLock()
    def get(self, user_key: str) -> FortuneHubState:
        with self._lock:
            state = self._states.get(user_key)
            if state is None:
                state = FortuneHubState(user_key=user_key)
                self._states[user_key] = state
            return state
    def set_theme(
        self,
        user_key: str,
        theme: str,
    ) -> FortuneHubState:
        state = self.get(user_key)
        with self._lock:
            state.theme = theme
        return state
    def set_question(
        self,
        user_key: str,
        question: str,
    ) -> FortuneHubState:
        state = self.get(user_key)
        with self._lock:
            state.last_question = question
        return state
    def remember_result(
        self,
        user_key: str,
        result_id: str,
    ) -> FortuneHubState:
        state = self.get(user_key)
        with self._lock:
            state.remember_result(result_id)
        return state
    def add_favorite(
        self,
        user_key: str,
        result_id: str,
    ) -> FortuneHubState:
        state = self.get(user_key)
        with self._lock:
            state.add_favorite(result_id)
        return state
    def remove_favorite(
        self,
        user_key: str,
        result_id: str,
    ) -> FortuneHubState:
        state = self.get(user_key)
        with self._lock:
            state.remove_favorite(result_id)
        return state