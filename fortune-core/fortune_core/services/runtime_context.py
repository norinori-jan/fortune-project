from __future__ import annotations
import hashlib
import json
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.models.runtime_context import FortuneRuntimeContext
class FortuneRuntimeContextService:
    def create(
        self,
        request: HubRuntimeRequest,
    ) -> FortuneRuntimeContext:
        request_id = self._request_id(request)
        return FortuneRuntimeContext(
            request_id=request_id,
            user_key=request.user_key,
            theme=request.theme,
            operation=request.operation,
            question=request.question,
            locale=str(request.metadata.get("locale", "ja-JP")),
            metadata=dict(request.metadata),
        )
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
        ).hexdigest()[:24]
