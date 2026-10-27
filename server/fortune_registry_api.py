from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from fortune_core.platform import (
    FortuneRunner,
    create_default_registry,
)
router = APIRouter(
    prefix="/fortune",
    tags=["fortune-registry"],
)
_registry = create_default_registry()
_runner = FortuneRunner(_registry)
class ProviderRequest(BaseModel):
    question: str | None = None
    orientation: str = "auto"
@router.get("/providers")
def providers() -> dict:
    return {
        "providers": [
            {
                "name": info.name,
                "title": info.title,
                "description": info.description,
                "categories": list(info.categories),
            }
            for info in _registry.infos()
        ]
    }
@router.post("/{provider}")
def run_provider(
    provider: str,
    request: ProviderRequest,
) -> dict:
    if not _registry.has(provider):
        raise HTTPException(
            status_code=404,
            detail=f"Unknown fortune provider: {provider}",
        )
    kwargs = {}
    if request.question is not None:
        kwargs["question"] = request.question
    if provider == "tarot":
        kwargs["orientation"] = request.orientation
    try:
        execution = _runner.run(
            provider,
            **kwargs,
        )
    except (ValueError, TypeError, KeyError) as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc
    return execution.to_dict()