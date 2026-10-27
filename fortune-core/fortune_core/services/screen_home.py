from __future__ import annotations

from typing import Any

from fortune_core.services.hub_page import (
    FortuneHubPageService,
)
from fortune_core.services.theme_tabs import (
    FortuneThemeTabService,
)
from fortune_core.services.ui_navigation import (
    FortuneUiNavigationService,
)


class FortuneHomeScreenService:
    def __init__(self) -> None:
        self.page = FortuneHubPageService()
        self.navigation = FortuneUiNavigationService()
        self.themes = FortuneThemeTabService()

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> dict[str, Any]:
        return {
            "screen": "home",
            "navigation": [
                item.to_dict()
                for item in self.navigation.build("home")
            ],
            "themes": [
                item.to_dict()
                for item in self.themes.build(theme)
            ],
            "page": self.page.home(
                user_key=user_key,
                theme=theme,
            ).to_dict(),
        }