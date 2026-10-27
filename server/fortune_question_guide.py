from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.question_guide import (
    FortuneQuestionGuideService,
)


router = APIRouter(
    prefix="/fortune/question-guide",
    tags=["fortune-question-guide"],
)

_service = FortuneQuestionGuideService()


@router.get("")
def question_guides() -> list[dict]:
    return [
        item.to_dict()
        for item in _service.list()
    ]


@router.get("/{theme}")
def question_guide(
    theme: str,
) -> dict:
    return _service.get(theme).to_dict()