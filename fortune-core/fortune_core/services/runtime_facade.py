from __future__ import annotations
from typing import Any
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_errors import FortuneRuntimeException
from fortune_core.services.runtime_gateway import FortuneRuntimeGateway
from fortune_core.services.runtime_health import FortuneRuntimeHealthService
from fortune_core.services.runtime_response import (
    FortuneRuntimeResponseService,
)
from fortune_core.services.runtime_router import FortuneRuntimeRouter
class FortuneRuntimeFacade:
    def __init__(
        self,
        gateway: FortuneRuntimeGateway | None = None,
        router: FortuneRuntimeRouter | None = None,
        health: FortuneRuntimeHealthService | None = None,
    ) -> None:
        self.gateway = gateway or FortuneRuntimeGateway()
        self.router = router or FortuneRuntimeRouter()
        self.health_service = health or FortuneRuntimeHealthService(
            metrics=self.gateway.pipeline.metrics,
        )
        self.response_service = FortuneRuntimeResponseService()
    def execute(
        self,
        request: HubRuntimeRequest,
    ) -> dict[str, Any]:
        normalized = self.router.normalize(request)
        try:
            self.router.validate(normalized)
            response = self.gateway.execute(normalized)
            from fortune_core.models.hub_runtime import HubRuntimeResponse
            model = HubRuntimeResponse(
                request_id=response["request_id"],
                operation=response["operation"],
                user_key=response["user_key"],
                theme=response["theme"],
                cached=response.get("cached", False),
                result=response.get("result", {}),
                metadata=response.get("metadata", {}),
            )
            return self.response_service.success(model)
        except FortuneRuntimeException as exc:
            return self.response_service.failure(exc)
    def health(self) -> dict[str, Any]:
        return self.health_service.health().to_dict()
