from __future__ import annotations
import hashlib
import json
from typing import Any
from fortune_core.models.hub_runtime import (
    HubRuntimeRequest,
    HubRuntimeResponse,
)
from fortune_core.services.hub import FortuneHubService
from fortune_core.services.hub_cache import FortuneHubCache
from fortune_core.services.hub_events import FortuneHubEventService
class FortuneHubRuntimeService:
    """
    Front-facing runtime coordinator.
    It does not replace individual fortune services.
    It coordinates them and adds:
    - deterministic request IDs
    - cache
    - event recording
    - operation dispatch
    """
    def __init__(
        self,
        hub: FortuneHubService | None = None,
        cache: FortuneHubCache | None = None,
        events: FortuneHubEventService | None = None,
    ) -> None:
        self.hub = hub or FortuneHubService()
        self.cache = cache or FortuneHubCache()
        self.events = events or FortuneHubEventService()
    def execute(self, request: HubRuntimeRequest) -> HubRuntimeResponse:
        request_id = self._request_id(request)
        cache_key = self._cache_key(request)
        if request.use_cache:
            cached = self.cache.get(cache_key)
            if cached is not None:
                self.events.emit(
                    event_type="cache_hit",
                    user_key=request.user_key,
                    operation=request.operation,
                    theme=request.theme,
                    payload={"request_id": request_id},
                )
                return HubRuntimeResponse(
                    request_id=request_id,
                    operation=request.operation,
                    user_key=request.user_key,
                    theme=request.theme,
                    cached=True,
                    result=cached,
                    metadata={"cache_key": cache_key},
                )
        result = self._dispatch(request)
        if request.use_cache:
            self.cache.set(cache_key, result)
        self.events.emit(
            event_type="fortune_executed",
            user_key=request.user_key,
            operation=request.operation,
            theme=request.theme,
            payload={"request_id": request_id},
        )
        return HubRuntimeResponse(
            request_id=request_id,
            operation=request.operation,
            user_key=request.user_key,
            theme=request.theme,
            cached=False,
            result=result,
            metadata={"cache_key": cache_key},
        )
    def _dispatch(self, request: HubRuntimeRequest) -> dict[str, Any]:
        operation = request.operation.lower()
        if operation == "home":
            result = self.hub.home(
                user_key=request.user_key,
                theme=request.theme,
            )
        elif operation == "quick":
            result = self.hub.quick(
                user_key=request.user_key,
                question=request.question,
                theme=request.theme,
            )
        elif operation == "today":
            result = self.hub.today(
                user_key=request.user_key,
                theme=request.theme,
            )
        else:
            raise ValueError(f"unsupported hub operation: {request.operation}")
        if hasattr(result, "to_dict"):
            return result.to_dict()
        if isinstance(result, dict):
            return result
        return {"value": result}
    @staticmethod
    def _request_id(request: HubRuntimeRequest) -> str:
        payload = {
            "user_key": request.user_key,
            "question": request.question,
            "theme": request.theme,
            "operation": request.operation,
            "metadata": request.metadata,
        }
        return hashlib.sha256(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()[:20]
    @staticmethod
    def _cache_key(request: HubRuntimeRequest) -> str:
        payload = {
            "user_key": request.user_key,
            "question": request.question,
            "theme": request.theme,
            "operation": request.operation,
        }
        return hashlib.sha256(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
            ).encode("utf-8")
        ).hexdigest()