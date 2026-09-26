from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.api_envelope import (
    FortuneApiEnvelopeService,
)
from fortune_core.services.fortune_batch import FortuneBatchService
router = APIRouter(
    prefix="/fortune/run",
    tags=["fortune-run"],
)
_envelope = FortuneApiEnvelopeService()
_batch = FortuneBatchService()
class FortuneRunRequest(BaseModel):
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
def run(
    request: FortuneRunRequest,
) -> dict[str, Any]:
    try:
        result = _batch.execute(
            question=request.question,
            theme=request.theme,
            providers=(
                tuple(request.providers)
                if request.providers
                else None
            ),
        )
        return _envelope.success(
            data=result,
            question=request.question,
            theme=request.theme,
            system_count=len(result.results),
        ).to_dict()
    except Exception as exc:
        return _envelope.failure(
            error=str(exc),
            question=request.question,
            theme=request.theme,
        ).to_dict()
