from __future__ import annotations

from fortune_core.models.ui_action import FortuneUiAction


class FortuneUiActionService:
    def home_actions(
        self,
        theme: str,
    ) -> list[FortuneUiAction]:
        return [
            FortuneUiAction(
                key="ask",
                label="質問して占う",
                action_type="navigate",
                target="/fortune/ui/question",
                payload={"theme": theme},
            ),
            FortuneUiAction(
                key="tarot",
                label="タロットを引く",
                action_type="navigate",
                target="/fortune/tarot",
                payload={"theme": theme},
            ),
            FortuneUiAction(
                key="today",
                label="今日の運勢",
                action_type="navigate",
                target="/fortune/content/today",
                payload={"theme": theme},
            ),
            FortuneUiAction(
                key="history",
                label="履歴を見る",
                action_type="navigate",
                target="/fortune/runtime-history",
                payload={},
            ),
            FortuneUiAction(
                key="favorites",
                label="お気に入り",
                action_type="navigate",
                target="/fortune/runtime-favorites",
                payload={},
            ),
        ]