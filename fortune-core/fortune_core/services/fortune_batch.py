from __future__ import annotations
from ..models.fortune_batch import FortuneBatchResult
from .provider_executor import FortuneProviderExecutor
class FortuneBatchService:
    DEFAULT_PROVIDERS = (
        "unified",
        "tarot",
        "meihua",
        "five-elements",
    )
    OPERATIONS = {
        "unified": "divine",
        "tarot": "draw",
        "meihua": "divine",
        "five-elements": "analyze",
    }
    def __init__(self) -> None:
        self.executor = FortuneProviderExecutor()
    def execute(
        self,
        *,
        question: str = "",
        theme: str = "general",
        providers: tuple[str, ...] | None = None,
    ) -> FortuneBatchResult:
        requested = providers or self.DEFAULT_PROVIDERS
        results = []
        for provider in requested:
            operation = self.OPERATIONS.get(
                provider,
                "divine",
            )
            results.append(
                self.executor.execute(
                    provider=provider,
                    operation=operation,
                    question=question,
                    theme=theme,
                )
            )
        return FortuneBatchResult(
            theme=theme,
            question=question,
            requested_providers=tuple(requested),
            results=tuple(results),
        )