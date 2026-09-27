from __future__ import annotations

from typing import Any

from fortune_core.services.system_selector import (
    FortuneSystemSelectorService,
)
from fortune_core.services.ui_actions import (
    FortuneUiActionService,
)


class FortuneThemeUiService:
    THEMES = (
        "general",
        "love",
        "work",
        "money",
        "health",
    )

    def __init__(self) -> None:
        self.systems = FortuneSystemSelectorService()
        self.actions = FortuneUiActionService()

    def build(
        self,
        theme: str,
    ) -> dict[str, Any]:
        if theme not in self.THEMES:
            theme = "general"

        return {
            "theme": theme,
            "themes": list(self.THEMES),
            "systems": [
                item.to_dict()
                for item in self.systems.list(theme)
            ],
            "actions": [
                item.to_dict()
                for item in self.actions.home_actions(theme)
            ],
        }