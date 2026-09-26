from __future__ import annotations
from typing import Any
from .fortune_registry import FortuneProviderRegistry
from .fortune_runner import FortuneExecution, FortuneRunner
from .settings import FortunePlatformSettings
from ..services.fortune_history import FortuneHistoryService
class FortuneApplication:
    def __init__(
        self,
        registry: FortuneProviderRegistry,
        settings: FortunePlatformSettings | None = None,
    ) -> None:
        self.settings = settings or FortunePlatformSettings()
        self.registry = registry
        self.runner = FortuneRunner(registry)
        self.history = FortuneHistoryService(
            max_items=self.settings.max_history_items
        )
    def run(
        self,
        provider: str,
        **kwargs: Any,
    ) -> FortuneExecution:
        execution = self.runner.run(
            provider,
            **kwargs,
        )
        if self.settings.history_enabled:
            question = kwargs.get("question", "")
            self.history.add(
                system=provider,
                question=question,
                result=execution.to_dict(),
            )
        return execution
    def providers(self) -> list[dict[str, Any]]:
        return [
            {
                "name": info.name,
                "title": info.title,
                "description": info.description,
                "categories": list(info.categories),
            }
            for info in self.registry.infos()
        ]