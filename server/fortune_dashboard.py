from __future__ import annotations
from datetime import date
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.dashboard_fortune import FortuneDashboardService
router = APIRouter(
    prefix="/fortune/dashboard",
    tags=["fortune-dashboard"],
)
_service = FortuneDashboardService()
class DashboardRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
    target_date: date | None = None
class DashboardResponse(BaseModel):
    title: str
    date_key: str
    daily: dict
    weekly: dict
    yearly: dict
    themes: list[dict]
    overall_message: str
    overall_advice: str
@router.post("", response_model=DashboardResponse)
def create_dashboard(request: DashboardRequest) -> DashboardResponse:
    result = _service.build(
        question=request.question,
        target_date=request.target_date,
    )
    return DashboardResponse(**result.to_dict())