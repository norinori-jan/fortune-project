from __future__ import annotations

from typing import Any

from fortune_core.services.theme_tabs import (
    FortuneThemeTabService,
)
from fortune_core.services.today_view import (
    FortuneTodayViewService,
)
from fortune_core.services.ui_navigation import (
    FortuneUiNavigationService,
)


class FortuneTodayScreenService:
    def __init__(self) -> None:
        self.today = FortuneTodayViewService()
        self.navigation = FortuneUiNavigationService()
        self.themes = FortuneThemeTabService()

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> dict[str, Any]:
        return {
            "screen": "today",
            "navigation": [
                item.to_dict()
                for item in self.navigation.build("today")
            ],
            "themes": [
                item.to_dict()
                for item in self.themes.build(theme)
            ],
            "today": self.today.build(
                user_key=user_key,
                theme=theme,
            ).to_dict(),
        }