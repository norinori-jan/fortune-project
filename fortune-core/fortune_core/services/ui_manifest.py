from __future__ import annotations

from typing import Any

from fortune_core.services.system_selector import (
    FortuneSystemSelectorService,
)


class FortuneUiManifestService:
    def __init__(self) -> None:
        self.systems = FortuneSystemSelectorService()

    def build(self) -> dict[str, Any]:
        return {
            "name": "fortune-hub",
            "version": "1.0.0",
            "themes": [
                "general",
                "love",
                "work",
                "money",
                "health",
            ],
            "systems": [
                item.to_dict()
                for item in self.systems.OPTIONS
            ],
            "pages": [
                "home",
                "today",
                "question",
                "result",
                "history",
                "favorites",
                "settings",
            ],
            "features": [
                "daily-fortune",
                "tarot",
                "meihua",
                "five-elements",
                "question-guide",
                "history",
                "favorites",
                "sharing",
            ],
        }