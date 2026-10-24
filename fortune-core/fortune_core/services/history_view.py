from __future__ import annotations

from typing import Any

from fortune_core.models.history_view import (
    FortuneHistoryViewItem,
)


class FortuneHistoryViewService:
    def build(
        self,
        item: dict[str, Any],
    ) -> FortuneHistoryViewItem:
        return FortuneHistoryViewItem(
            request_id=str(
                item.get("request_id", "")
            ),
            title=str(
                item.get(
                    "title",
                    item.get("operation", "占い結果"),
                )
            ),
            theme=str(
                item.get("theme", "general")
            ),
            operation=str(
                item.get("operation", "")
            ),
            question=str(
                item.get("question", "")
            ),
            created_at=str(
                item.get("created_at", "")
            ),
            result=dict(
                item.get("result", {})
            ),
        )

    def list(
        self,
        items: list[dict[str, Any]],
    ) -> list[FortuneHistoryViewItem]:
        return [
            self.build(item)
            for item in items
        ]