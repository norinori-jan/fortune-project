from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.comparison_run import (
    FortuneComparisonRunService,
)
router = APIRouter(
    prefix="/fortune/comparison-run",
    tags=["fortune-comparison"],
)
_service = FortuneComparisonRunService()
class FortuneComparisonRunRequest(BaseModel):
    question: str = Field(
        default="",
        max_length=500,
    )
    theme: str = Field(
        default="general",
        max_length=50,
    )
    providers: list[str] | None = Field(
        default=None,
        max_length=10,
    )
@router.post("")
def comparison_run(
    request: FortuneComparisonRunRequest,
) -> dict[str, Any]:
    result = _service.execute(
        question=request.question,
        theme=request.theme,
        providers=(
            tuple(request.providers)
            if request.providers
            else None
        ),
    )
    return result.to_dict()