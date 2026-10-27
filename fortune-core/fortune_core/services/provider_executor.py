from __future__ import annotations
from typing import Any
from ..models.fortune_provider_result import FortuneProviderResult
from ..platform.providers import create_default_registry
class FortuneProviderExecutor:
    def __init__(self) -> None:
        self.registry = create_default_registry()
    def execute(
        self,
        *,
        provider: str,
        operation: str,
        question: str = "",
        theme: str = "general",
        **kwargs: Any,
    ) -> FortuneProviderResult:
        try:
            target = self.registry.get(provider)
            if operation == "divine":
                result = target.divine(
                    question=question,
                    theme=theme,
                    **kwargs,
                )
            elif operation == "draw":
                result = target.draw(
                    question=question,
                    theme=theme,
                    **kwargs,
                )
            elif operation == "analyze":
                result = target.analyze(
                    question=question,
                    theme=theme,
                    **kwargs,
                )
            else:
                raise ValueError(
                    f"Unsupported operation: {operation}"
                )
            return FortuneProviderResult(
                provider=provider,
                system=provider,
                success=True,
                result=self._as_dict(result),
            )
        except Exception as exc:
            return FortuneProviderResult(
                provider=provider,
                system=provider,
                success=False,
                result={},
                error=str(exc),
            )
    @staticmethod
    def _as_dict(value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return value
        if hasattr(value, "to_dict"):
            result = value.to_dict()
            if isinstance(result, dict):
                return result
        if hasattr(value, "__dict__"):
            return dict(value.__dict__)
        return {"value": value}