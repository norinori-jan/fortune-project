from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.ui_state import (
    FortuneUiStateService,
)


router = APIRouter(
    prefix="/fortune/ui-state",
    tags=["fortune-ui-state"],
)

_service = FortuneUiStateService()


@router.get("/{user_key}")
def get_state(
    user_key: str,
) -> dict:
    return _service.get(user_key).to_dict()


@router.post("/{user_key}/theme")
def set_theme(
    user_key: str,
    theme: str,
) -> dict:
    return _service.set_theme(
        user_key,
        theme,
    ).to_dict()


@router.post("/{user_key}/system")
def set_system(
    user_key: str,
    system: str,
) -> dict:
    return _service.set_system(
        user_key,
        system,
    ).to_dict()


@router.post("/{user_key}/page")
def set_page(
    user_key: str,
    page: str,
) -> dict:
    return _service.set_page(
        user_key,
        page,
    ).to_dict()


@router.post("/{user_key}/question")
def set_question(
    user_key: str,
    question: str,
) -> dict:
    return _service.set_question(
        user_key,
        question,
    ).to_dict()


@router.post("/{user_key}/result")
def set_result(
    user_key: str,
    result_id: str,
) -> dict:
    return _service.set_result(
        user_key,
        result_id,
    ).to_dict()