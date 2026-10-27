from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.services.compatibility import CompatibilityService
router = APIRouter(
    prefix="/fortune/compatibility",
    tags=["fortune-compatibility"],
)
_service = CompatibilityService()
class CompatibilityRequest(BaseModel):
    person_a: str = Field(..., min_length=1, max_length=100)
    person_b: str = Field(..., min_length=1, max_length=100)
    theme: str = "general"
class CompatibilityResponse(BaseModel):
    score: int
    title: str
    message: str
    advice: str
    keywords: list[str]
@router.post(
    "",
    response_model=CompatibilityResponse,
)
def create_compatibility(
    request: CompatibilityRequest,
) -> CompatibilityResponse:
    result = _service.build(
        person_a=request.person_a,
        person_b=request.person_b,
        theme=request.theme,
    )
    return CompatibilityResponse(**result.to_dict())
