from __future__ import annotations
from datetime import date
from fastapi import APIRouter, HTTPException
from fortune_core.services.five_elements import FiveElementService
from fortune_core.services.meihua_fortune import MeihuaFortuneService
from fortune_core.services.shichu_profile import ShichuProfileService
from fortune_core.services.tarot_fortune import TarotFortuneService
from .fortune_models import (
    ElementRequest,
    MeihuaRequest,
    ShichuRequest,
    TarotRequest,
)
router = APIRouter(
    prefix="/fortune",
    tags=["fortune-services"],
)
tarot_service = TarotFortuneService()
meihua_service = MeihuaFortuneService()
element_service = FiveElementService()
shichu_service = ShichuProfileService()
@router.post("/tarot")
def tarot(request: TarotRequest) -> dict:
    result = tarot_service.draw(
        question=request.question,
        orientation=request.orientation,
    )
    return result.to_dict()
@router.post("/meihua")
def meihua(request: MeihuaRequest) -> dict:
    result = meihua_service.divine(request.question)
    return result.to_dict()
@router.post("/five-elements")
def five_elements(request: ElementRequest) -> dict:
    result = element_service.analyze(request.text)
    return result.to_dict()
@router.post("/shichu/profile")
def shichu_profile(request: ShichuRequest) -> dict:
    try:
        birth_date = date.fromisoformat(request.birth_date)
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail="Invalid birth_date",
        ) from exc
    result = shichu_service.create(birth_date)
    return result.to_dict()
