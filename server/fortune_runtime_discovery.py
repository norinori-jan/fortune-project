from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_discovery import (
    FortuneRuntimeDiscoveryService,
)
from fortune_core.services.runtime_help import (
    FortuneRuntimeHelpService,
)


router = APIRouter(
    prefix="/fortune/discovery",
    tags=["fortune-discovery"],
)

_discovery = FortuneRuntimeDiscoveryService()
_help = FortuneRuntimeHelpService()


@router.get("")
def discovery(
    category: str | None = None,
    theme: str | None = None,
) -> list[dict]:
    return [
        item.to_dict()
        for item in _discovery.list(
            category=category,
            theme=theme,
        )
    ]


@router.get("/search")
def discovery_search(
    q: str,
) -> list[dict]:
    return [
        item.to_dict()
        for item in _discovery.search(q)
    ]


@router.get("/help")
def discovery_help() -> list[dict]:
    return [
        item.to_dict()
        for item in _help.list()
    ]


@router.get("/help/{key}")
def discovery_help_item(
    key: str,
) -> dict | None:
    item = _help.get(key)
    return item.to_dict() if item else None