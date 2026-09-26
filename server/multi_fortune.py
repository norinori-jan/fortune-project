from __future__ import annotations
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.multi_fortune import MultiFortuneService
router = APIRouter(
    prefix="/fortune",
    tags=["multi-fortune"],
)
service = MultiFortuneService()
class MultiFortuneRequest(BaseModel):
    question: str = Field(min_length=1)
    theme: str = "general"
@router.post("/multi")
def multi_fortune(
    request: MultiFortuneRequest,
) -> dict:
    result = service.divine(
        question=request.question,
        theme=request.theme,
    )
    return result.to_dict()