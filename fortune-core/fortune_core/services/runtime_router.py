from __future__ import annotations
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_errors import (
    EmptyQuestionError,
    InvalidThemeError,
    UnsupportedOperationError,
)
class FortuneRuntimeRouter:
    OPERATIONS = {
        "home",
        "quick",
        "today",
    }
    THEMES = {
        "general",
        "love",
        "work",
        "money",
        "health",
    }
    def validate(self, request: HubRuntimeRequest) -> None:
        operation = request.operation.lower()
        theme = request.theme.lower()
        if operation not in self.OPERATIONS:
            raise UnsupportedOperationError(operation)
        if theme not in self.THEMES:
            raise InvalidThemeError(theme)
        if operation == "quick" and not request.question.strip():
            raise EmptyQuestionError()
    def normalize(
        self,
        request: HubRuntimeRequest,
    ) -> HubRuntimeRequest:
        return HubRuntimeRequest(
            user_key=request.user_key.strip() or "anonymous",
            question=request.question.strip(),
            theme=request.theme.strip().lower() or "general",
            operation=request.operation.strip().lower() or "home",
            use_cache=request.use_cache,
            metadata=dict(request.metadata),
        )
