from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services import UnifiedFortuneService
router = APIRouter(
    prefix="/fortune",
    tags=["fortune"],
)
service = UnifiedFortuneService()
class UnifiedFortuneRequest(BaseModel):
    question: str = Field(min_length=1)
    theme: str = "general"
class UnifiedFortuneResponse(BaseModel):
    question: str
    theme: str
    overall: str
    message: str
    items: list[dict]
    keywords: list[str]
    advice: list[str]
@router.post("/unified", response_model=UnifiedFortuneResponse)
def unified_fortune(
    request: UnifiedFortuneRequest,
) -> UnifiedFortuneResponse:
    result = service.divine(
        question=request.question,
        theme=request.theme,
    )
    return UnifiedFortuneResponse(
        question=result.question,
        theme=result.theme,
        overall=result.overall,
        message=result.message,
        items=[
            {
                "system": item.system,
                "title": item.title,
                "summary": item.summary,
                "details": item.details,
            }
            for item in result.items
        ],
        keywords=result.keywords,
        advice=result.advice,
    )
