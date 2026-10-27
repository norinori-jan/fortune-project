from __future__ import annotations

from fastapi import APIRouter

from fortune_core.models.result_card import (
    FortuneResultCard,
)
from fortune_core.services.share_card import (
    FortuneShareCardService,
)


router = APIRouter(
    prefix="/fortune/share-card",
    tags=["fortune-share-card"],
)

_service = FortuneShareCardService()


@router.post("")
def share_card(
    card: dict,
) -> dict:
    result_card = FortuneResultCard(
        result_id=str(card.get("result_id", "")),
        title=str(card.get("title", "")),
        system=str(card.get("system", "")),
        theme=str(card.get("theme", "general")),
        headline=str(card.get("headline", "")),
        score=card.get("score"),
        message=str(card.get("message", "")),
        advice=str(card.get("advice", "")),
        keywords=tuple(
            str(x)
            for x in card.get("keywords", [])
        ),
        metadata=dict(
            card.get("metadata", {})
        ),
    )

    return _service.build(
        result_card
    ).to_dict()