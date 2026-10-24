from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.screen_home import (
    FortuneHomeScreenService,
)
from fortune_core.services.screen_today import (
    FortuneTodayScreenService,
)
from fortune_core.services.screen_question import (
    FortuneQuestionScreenService,
)
from fortune_core.services.screen_history import (
    FortuneHistoryScreenService,
)
from fortune_core.services.screen_favorites import (
    FortuneFavoritesScreenService,
)


router = APIRouter(
    prefix="/fortune/screens",
    tags=["fortune-screens"],
)

_home = FortuneHomeScreenService()
_today = FortuneTodayScreenService()
_question = FortuneQuestionScreenService()
_history = FortuneHistoryScreenService()
_favorites = FortuneFavoritesScreenService()


@router.get("/{user_key}/home")
def home(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _home.build(
        user_key=user_key,
        theme=theme,
    )


@router.get("/{user_key}/today")
def today(
    user_key: str,
    theme: str = "general",
) -> dict:
    return _today.build(
        user_key=user_key,
        theme=theme,
    )


@router.get("/question")
def question(
    theme: str = "general",
) -> dict:
    return _question.build(theme)


@router.get("/{user_key}/history")
def history(
    user_key: str,
    limit: int = 20,
) -> dict:
    return _history.build(
        user_key=user_key,
        limit=limit,
    )


@router.get("/{user_key}/favorites")
def favorites(
    user_key: str,
) -> dict:
    return _favorites.build(user_key)