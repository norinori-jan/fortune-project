from __future__ import annotations
from typing import Any
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_orchestrator import (
    FortuneRuntimeOrchestrator,
)
from fortune_core.services.runtime_recommendation import (
    FortuneRuntimeRecommendationService,
)
from fortune_core.services.runtime_summary import (
    FortuneRuntimeSummaryService,
)
from fortune_core.services.runtime_user_state import (
    FortuneRuntimeUserStateService,
)
class FortuneRuntimeUserService:
    def __init__(
        self,
        orchestrator: FortuneRuntimeOrchestrator | None = None,
        state: FortuneRuntimeUserStateService | None = None,
        summary: FortuneRuntimeSummaryService | None = None,
        recommendations: FortuneRuntimeRecommendationService | None = None,
    ) -> None:
        self.orchestrator = (
            orchestrator
            or FortuneRuntimeOrchestrator()
        )
        self.state = (
            state
            or FortuneRuntimeUserStateService()
        )
        self.summary = (
            summary
            or FortuneRuntimeSummaryService(
                self.orchestrator.history
            )
        )
        self.recommendations = (
            recommendations
            or FortuneRuntimeRecommendationService()
        )
    def execute(
        self,
        request: HubRuntimeRequest,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        result = self.orchestrator.execute(request)
        request_id = result.get("request_id")
        self.state.update(
            request.user_key,
            session_id=session_id,
            theme=request.theme,
            request_id=request_id,
        )
        return result
    def profile(self, user_key: str) -> dict[str, Any]:
        return self.state.get(user_key).to_dict()
    def summary_for(self, user_key: str) -> dict[str, Any]:
        return self.summary.summarize(user_key).to_dict()
    def recommendations_for(
        self,
        user_key: str,
        themes: list[str] | None = None,
    ) -> list[dict[str, Any]]:
        return [
            item.to_dict()
            for item in self.recommendations.list(
                user_key=user_key,
                themes=themes,
            )
        ]
