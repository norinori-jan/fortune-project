from __future__ import annotations

from typing import Any

from fastapi import APIRouter
from pydantic import BaseModel

from fortune_core.services.runtime_favorites import (
    FortuneRuntimeFavoriteService,
)


router = APIRouter(
    prefix="/fortune/runtime-favorites",
    tags=["fortune-runtime-favorites"],
)

_service = FortuneRuntimeFavoriteService()


class FavoriteRequest(BaseModel):
    user_key: str
    title: str
    system: str
    theme: str = "general"
    question: str = ""
    result: dict[str, Any]


@router.post("")
def add_favorite(
    payload: FavoriteRequest,
) -> dict:
    return _service.add(
        user_key=payload.user_key,
        title=payload.title,
        system=payload.system,
        theme=payload.theme,
        question=payload.question,
        result=payload.result,
    ).to_dict()


@router.get("/{user_key}")
def list_favorites(
    user_key: str,
) -> list[dict]:
    return [
        item.to_dict()
        for item in _service.list(user_key)
    ]


@router.delete("/{favorite_id}")
def remove_favorite(
    favorite_id: str,
    user_key: str | None = None,
) -> dict:
    return {
        "favorite_id": favorite_id,
        "removed": _service.remove(
            favorite_id,
            user_key=user_key,
        ),
    }