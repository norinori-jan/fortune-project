from __future__ import annotations

from threading import RLock

from fortune_core.models.ui_state import FortuneUiState


class FortuneUiStateService:
    def __init__(self) -> None:
        self._states: dict[str, FortuneUiState] = {}
        self._lock = RLock()

    def get(self, user_key: str) -> FortuneUiState:
        with self._lock:
            if user_key not in self._states:
                self._states[user_key] = FortuneUiState(
                    user_key=user_key
                )
            return self._states[user_key]

    def set_theme(
        self,
        user_key: str,
        theme: str,
    ) -> FortuneUiState:
        state = self.get(user_key)
        with self._lock:
            state.theme = theme
            return state

    def set_system(
        self,
        user_key: str,
        system: str,
    ) -> FortuneUiState:
        state = self.get(user_key)
        with self._lock:
            state.active_system = system
            return state

    def set_page(
        self,
        user_key: str,
        page: str,
    ) -> FortuneUiState:
        state = self.get(user_key)
        with self._lock:
            state.active_page = page
            return state

    def set_question(
        self,
        user_key: str,
        question: str,
    ) -> FortuneUiState:
        state = self.get(user_key)
        with self._lock:
            state.question = question
            return state

    def set_result(
        self,
        user_key: str,
        result_id: str,
    ) -> FortuneUiState:
        state = self.get(user_key)
        with self._lock:
            state.selected_result_id = result_id
            return state