from __future__ import annotations

from typing import Any

from fortune_core.services.favorites_view import (
    FortuneFavoritesViewService,
)
from fortune_core.services.ui_navigation import (
    FortuneUiNavigationService,
)


class FortuneFavoritesScreenService:
    def __init__(self) -> None:
        self.favorites = FortuneFavoritesViewService()
        self.navigation = FortuneUiNavigationService()

    def build(
        self,
        user_key: str,
    ) -> dict[str, Any]:
        view = self.favorites.build(user_key)

        return {
            "screen": "favorites",
            "navigation": [
                item.to_dict()
                for item in self.navigation.build(
                    "favorites"
                )
            ],
            "favorites": view.to_dict(),
        }