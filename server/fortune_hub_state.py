from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.hub_state import FortuneHubStateService
router = APIRouter(
    prefix="/fortune/hub/state",
    tags=["fortune-hub-state"],
)
_service = FortuneHubStateService()
class ThemeStateRequest(BaseModel):
    user_key: str = Field(min_length=1, max_length=200)
    theme: str = Field(default="general", max_length=50)
class QuestionStateRequest(BaseModel):
    user_key: str = Field(min_length=1, max_length=200)
    question: str = Field(default="", max_length=500)
class ResultStateRequest(BaseModel):
    user_key: str = Field(min_length=1, max_length=200)
    result_id: str = Field(min_length=1, max_length=200)
@router.get("")
def get_state(
    user_key: str,
) -> dict[str, Any]:
    return _service.get(user_key).to_dict()
@router.post("/theme")
def set_theme(
    request: ThemeStateRequest,
) -> dict[str, Any]:
    return _service.set_theme(
        request.user_key,
        request.theme,
    ).to_dict()
@router.post("/question")
def set_question(
    request: QuestionStateRequest,
) -> dict[str, Any]:
    return _service.set_question(
        request.user_key,
        request.question,
    ).to_dict()
@router.post("/result")
def remember_result(
    request: ResultStateRequest,
) -> dict[str, Any]:
    return _service.remember_result(
        request.user_key,
        request.result_id,
    ).to_dict()
@router.post("/favorite")
def add_favorite(
    request: ResultStateRequest,
) -> dict[str, Any]:
    return _service.add_favorite(
        request.user_key,
        request.result_id,
    ).to_dict()
@router.delete("/favorite")
def remove_favorite(
    request: ResultStateRequest,
) -> dict[str, Any]:
    return _service.remove_favorite(
        request.user_key,
        request.result_id,
    ).to_dict()