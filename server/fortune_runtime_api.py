from __future__ import annotations
from typing import Any
from fastapi import APIRouter
from pydantic import BaseModel, Field
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.batch_runtime import FortuneBatchRuntimeService
from fortune_core.services.runtime_pipeline import FortuneRuntimePipeline
from fortune_core.services.service_manifest import FortuneServiceManifestService
router = APIRouter(
    prefix="/fortune/runtime",
    tags=["fortune-runtime"],
)
_pipeline = FortuneRuntimePipeline()
_batch = FortuneBatchRuntimeService(_pipeline)
_manifest = FortuneServiceManifestService()
class RuntimeBatchRequest(BaseModel):
    requests: list[dict[str, Any]] = Field(default_factory=list)
@router.post("/execute")
def execute_runtime(
    user_key: str = "anonymous",
    question: str = "",
    theme: str = "general",
    operation: str = "home",
    use_cache: bool = True,
) -> dict[str, Any]:
    request = HubRuntimeRequest(
        user_key=user_key,
        question=question,
        theme=theme,
        operation=operation,
        use_cache=use_cache,
    )
    return _pipeline.execute_dict(request)
@router.post("/batch")
def execute_runtime_batch(
    payload: RuntimeBatchRequest,
) -> list[dict[str, Any]]:
    requests = [
        HubRuntimeRequest(
            user_key=str(item.get("user_key", "anonymous")),
            question=str(item.get("question", "")),
            theme=str(item.get("theme", "general")),
            operation=str(item.get("operation", "home")),
            use_cache=bool(item.get("use_cache", True)),
            metadata=dict(item.get("metadata", {})),
        )
        for item in payload.requests
    ]
    return [
        {
            "index": item.index,
            "success": item.success,
            "result": item.result,
            "error": item.error,
        }
        for item in _batch.execute(requests)
    ]
@router.get("/metrics")
def runtime_metrics() -> dict[str, Any]:
    return _pipeline.metrics.snapshot().to_dict()
@router.get("/manifest")
def runtime_manifest() -> list[dict[str, Any]]:
    return [
        item.to_dict()
        for item in _manifest.list()
    ]
