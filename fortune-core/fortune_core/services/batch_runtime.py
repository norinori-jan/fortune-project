from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_pipeline import FortuneRuntimePipeline
@dataclass(frozen=True)
class RuntimeBatchItem:
    index: int
    success: bool
    result: dict[str, Any] | None = None
    error: str | None = None
class FortuneBatchRuntimeService:
    def __init__(
        self,
        pipeline: FortuneRuntimePipeline | None = None,
    ) -> None:
        self.pipeline = pipeline or FortuneRuntimePipeline()
    def execute(
        self,
        requests: list[HubRuntimeRequest],
    ) -> list[RuntimeBatchItem]:
        results: list[RuntimeBatchItem] = []
        for index, request in enumerate(requests):
            try:
                result = self.pipeline.execute(request)
                results.append(
                    RuntimeBatchItem(
                        index=index,
                        success=True,
                        result=result.to_dict(),
                    )
                )
            except Exception as exc:
                results.append(
                    RuntimeBatchItem(
                        index=index,
                        success=False,
                        error=str(exc),
                    )
                )
        return results
