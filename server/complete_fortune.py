from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.complete_fortune import CompleteFortuneService
router = APIRouter(
    prefix="/fortune",
    tags=["complete-fortune"],
)
service = CompleteFortuneService()
class CompleteFortuneRequest(BaseModel):
    question: str = Field(min_length=1)
class CompleteFortuneResponse(BaseModel):
    question: str
    theme: str
    overall: str
    message: str
    items: list[dict]
    keywords: list[str]
    advice: list[str]
@router.post(
    "/complete",
    response_model=CompleteFortuneResponse,
)
def complete_fortune(
    request: CompleteFortuneRequest,
) -> CompleteFortuneResponse:
    result = service.divine(request.question)
    return CompleteFortuneResponse(
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