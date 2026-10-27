from __future__ import annotations

from typing import Any

from fortune_core.services.runtime_history_items import (
    FortuneRuntimeHistoryItemService,
)
from fortune_core.services.history_view import (
    FortuneHistoryViewService,
)
from fortune_core.services.ui_navigation import (
    FortuneUiNavigationService,
)


class FortuneHistoryScreenService:
    def __init__(self) -> None:
        self.history = FortuneRuntimeHistoryItemService()
        self.view = FortuneHistoryViewService()
        self.navigation = FortuneUiNavigationService()

    def build(
        self,
        user_key: str,
        limit: int = 20,
    ) -> dict[str, Any]:
        items = self.history.list(
            user_key=user_key,
            limit=limit,
        )

        return {
            "screen": "history",
            "navigation": [
                item.to_dict()
                for item in self.navigation.build("history")
            ],
            "items": [
                item.to_dict()
                for item in self.view.list(
                    [item.to_dict() for item in items]
                )
            ],
        }