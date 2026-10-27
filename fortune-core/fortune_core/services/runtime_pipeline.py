from __future__ import annotations
from typing import Any
from fortune_core.models.hub_runtime import (
    HubRuntimeRequest,
    HubRuntimeResponse,
)
from fortune_core.services.hub_runtime import FortuneHubRuntimeService
from fortune_core.services.runtime_context import FortuneRuntimeContextService
from fortune_core.services.runtime_metrics import FortuneRuntimeMetricsService
class FortuneRuntimePipeline:
    def __init__(
        self,
        runtime: FortuneHubRuntimeService | None = None,
        context: FortuneRuntimeContextService | None = None,
        metrics: FortuneRuntimeMetricsService | None = None,
    ) -> None:
        self.runtime = runtime or FortuneHubRuntimeService()
        self.context = context or FortuneRuntimeContextService()
        self.metrics = metrics or FortuneRuntimeMetricsService()
    def execute(
        self,
        request: HubRuntimeRequest,
    ) -> HubRuntimeResponse:
        self.metrics.request_started()
        context = self.context.create(request)
        try:
            response = self.runtime.execute(request)
            if response.cached:
                self.metrics.cache_hit()
            else:
                self.metrics.cache_miss()
            self.metrics.request_succeeded()
            metadata = dict(response.metadata)
            metadata["runtime_context"] = context.to_dict()
            return HubRuntimeResponse(
                request_id=response.request_id,
                operation=response.operation,
                user_key=response.user_key,
                theme=response.theme,
                cached=response.cached,
                result=response.result,
                metadata=metadata,
            )
        except Exception:
            self.metrics.request_failed()
            raise
    def execute_dict(
        self,
        request: HubRuntimeRequest,
    ) -> dict[str, Any]:
        return self.execute(request).to_dict()
