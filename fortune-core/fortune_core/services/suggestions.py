from .question_suggestions import QuestionSuggestionService
__all__ = ["QuestionSuggestionService"]

server/fortune_suggestions.py

from fastapi import APIRouter
from pydantic import BaseModel
from fortune_core.services.question_suggestions import (
    QuestionSuggestionService,
)
router = APIRouter(
    prefix="/fortune/suggestions",
    tags=["fortune-suggestions"],
)
_service = QuestionSuggestionService()
class SuggestionResponse(BaseModel):
    question: str
    theme: str
    system: str
    reason: str
@router.get("", response_model=list[SuggestionResponse])
def get_suggestions(
    theme: str = "general",
) -> list[SuggestionResponse]:
    return [
        SuggestionResponse(**item.to_dict())
        for item in _service.suggest(theme)
    ]
