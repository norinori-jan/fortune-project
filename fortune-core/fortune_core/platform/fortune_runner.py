from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .fortune_registry import FortuneProviderRegistry
@dataclass(frozen=True, slots=True)
class FortuneExecution:
    provider: str
    result: Any
    def to_dict(self) -> dict[str, Any]:
        if hasattr(self.result, "to_dict"):
            result = self.result.to_dict()
        elif isinstance(self.result, dict):
            result = self.result
        else:
            result = {
                "value": self.result,
            }
        return {
            "provider": self.provider,
            "result": result,
        }
class FortuneRunner:
    def __init__(
        self,
        registry: FortuneProviderRegistry,
    ) -> None:
        self.registry = registry
    def run(
        self,
        provider: str,
        **kwargs: Any,
    ) -> FortuneExecution:
        target = self.registry.get(provider)
        method = getattr(target, "divine", None)
        if method is None:
            method = getattr(target, "draw", None)
        if method is None:
            method = getattr(target, "analyze", None)
        if method is None:
            raise TypeError(
                f"provider does not expose a supported method: {provider}"
            )
        result = method(**kwargs)
        return FortuneExecution(
            provider=provider,
            result=result,
        )