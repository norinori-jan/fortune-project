from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_pipeline import (
    FortunePipelineService,
)
router = APIRouter(
    prefix="/fortune/pipeline",
    tags=["fortune-pipeline"],
)
_service = FortunePipelineService()
class FortunePipelineRequest(BaseModel):
    question: str = Field(
        default="",
        max_length=500,
    )
    theme: str = Field(
        default="general",
        max_length=50,
    )
    user_key: str | None = Field(
        default=None,
        max_length=200,
    )
    birth_date: str | None = Field(
        default=None,
        max_length=20,
    )
@router.post("")
def execute_pipeline(
    request: FortunePipelineRequest,
) -> dict[str, Any]:
    result = _service.execute(
        user_key=request.user_key,
        birth_date=request.birth_date,
        question=request.question,
        theme=request.theme,
    )
    return result.to_dict()

