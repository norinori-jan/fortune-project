from __future__ import annotations
from typing import Any
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.models.runtime_request_record import (
    FortuneRuntimeRequestRecord,
)
from fortune_core.services.runtime_config import (
    FortuneRuntimeConfigService,
)
from fortune_core.services.runtime_facade import FortuneRuntimeFacade
from fortune_core.services.runtime_history import (
    FortuneRuntimeHistoryService,
)
from fortune_core.services.runtime_limiter import (
    FortuneRuntimeRateLimiter,
)
from fortune_core.services.theme_router import (
    FortuneThemeRouterService,
)
class FortuneRuntimeOrchestrator:
    """
    Runtime全体の入口。
    Facade:
        個別Runtime処理
    Orchestrator:
        設定
        レート制御
        テーマルーティング
        実行履歴
        最終レスポンス
    """
    def __init__(
        self,
        facade: FortuneRuntimeFacade | None = None,
        config: FortuneRuntimeConfigService | None = None,
        history: FortuneRuntimeHistoryService | None = None,
        limiter: FortuneRuntimeRateLimiter | None = None,
        theme_router: FortuneThemeRouterService | None = None,
    ) -> None:
        self.facade = facade or FortuneRuntimeFacade()
        self.config = config or FortuneRuntimeConfigService()
        self.history = history or FortuneRuntimeHistoryService()
        runtime_config = self.config.get()
        self.limiter = limiter or FortuneRuntimeRateLimiter(
            max_requests=runtime_config.max_requests_per_user,
        )
        self.theme_router = (
            theme_router
            or FortuneThemeRouterService()
        )
    def execute(
        self,
        request: HubRuntimeRequest,
    ) -> dict[str, Any]:
        normalized = HubRuntimeRequest(
            user_key=request.user_key.strip() or "anonymous",
            question=request.question.strip(),
            theme=request.theme.strip().lower() or "general",
            operation=request.operation.strip().lower() or "home",
            use_cache=request.use_cache,
            metadata=dict(request.metadata),
        )
        self.limiter.require(normalized.user_key)
        route = self.theme_router.get(normalized.theme)
        result = self.facade.execute(normalized)
        request_id = result.get("request_id", "")
        self.history.add(
            FortuneRuntimeRequestRecord(
                request_id=request_id,
                user_key=normalized.user_key,
                operation=normalized.operation,
                theme=normalized.theme,
                success=bool(result.get("success", False)),
                cached=bool(result.get("cached", False)),
                result=result.get("result", {}),
            )
        )
        result["runtime"] = {
            "theme_route": route.to_dict(),
            "remaining_requests": self.limiter.remaining(
                normalized.user_key
            ),
        }
        return result
