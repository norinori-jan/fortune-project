from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.fortune_compare import FortuneCompareService
router = APIRouter(
    prefix="/fortune/compare",
    tags=["fortune-compare"],
)
_service = FortuneCompareService()
class CompareRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)
class CompareResponse(BaseModel):
    question: str
    items: list[dict]
@router.post("", response_model=CompareResponse)
def compare_fortunes(
    request: CompareRequest,
) -> CompareResponse:
    result = _service.build(request.question)
    return CompareResponse(**result.to_dict())
