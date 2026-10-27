from __future__ import annotations

from fortune_core.models.favorites_view import (
    FortuneFavoritesView,
)
from fortune_core.services.runtime_favorites import (
    FortuneRuntimeFavoriteService,
)


class FortuneFavoritesViewService:
    def __init__(self) -> None:
        self.favorites = FortuneRuntimeFavoriteService()

    def build(
        self,
        user_key: str,
    ) -> FortuneFavoritesView:
        items = self.favorites.list(
            user_key=user_key
        )

        return FortuneFavoritesView(
            user_key=user_key,
            items=tuple(
                item.to_dict()
                for item in items
            ),
        )