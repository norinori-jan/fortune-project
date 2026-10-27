from __future__ import annotations
from typing import Any
from fortune_core.models.hub_runtime import HubRuntimeResponse
from fortune_core.services.runtime_errors import FortuneRuntimeException
class FortuneRuntimeResponseService:
    @staticmethod
    def success(
        response: HubRuntimeResponse,
    ) -> dict[str, Any]:
        return {
            "success": True,
            "request_id": response.request_id,
            "operation": response.operation,
            "user_key": response.user_key,
            "theme": response.theme,
            "cached": response.cached,
            "result": response.result,
            "metadata": response.metadata,
        }
    @staticmethod
    def failure(
        error: FortuneRuntimeException,
    ) -> dict[str, Any]:
        return {
            "success": False,
            "error": error.to_model().to_dict(),
        }