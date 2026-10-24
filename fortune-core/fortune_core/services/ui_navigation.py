from __future__ import annotations

from fortune_core.models.ui_navigation import (
    FortuneUiNavigationItem,
)


class FortuneUiNavigationService:
    ITEMS = (
        ("home", "ホーム", "/", "home"),
        ("today", "今日", "/today", "sun"),
        ("question", "占う", "/question", "sparkles"),
        ("history", "履歴", "/history", "clock"),
        ("favorites", "お気に入り", "/favorites", "heart"),
    )

    def build(
        self,
        active_page: str = "home",
    ) -> list[FortuneUiNavigationItem]:
        return [
            FortuneUiNavigationItem(
                key=key,
                label=label,
                path=path,
                icon=icon,
                active=key == active_page,
            )
            for key, label, path, icon in self.ITEMS
        ]