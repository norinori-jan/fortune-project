from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable
@dataclass(frozen=True, slots=True)
class FortuneProviderInfo:
    name: str
    title: str
    description: str
    categories: tuple[str, ...]
class FortuneProviderRegistry:
    def __init__(self) -> None:
        self._providers: dict[str, Any] = {}
        self._info: dict[str, FortuneProviderInfo] = {}
    def register(
        self,
        name: str,
        provider: Any,
        *,
        title: str | None = None,
        description: str = "",
        categories: tuple[str, ...] = (),
    ) -> None:
        key = name.strip().lower()
        if not key:
            raise ValueError("provider name must not be empty")
        if key in self._providers:
            raise ValueError(
                f"provider already registered: {key}"
            )
        self._providers[key] = provider
        self._info[key] = FortuneProviderInfo(
            name=key,
            title=title or key,
            description=description,
            categories=categories,
        )
    def get(self, name: str) -> Any:
        key = name.strip().lower()
        try:
            return self._providers[key]
        except KeyError as exc:
            raise KeyError(
                f"unknown fortune provider: {name}"
            ) from exc
    def info(self, name: str) -> FortuneProviderInfo:
        key = name.strip().lower()
        try:
            return self._info[key]
        except KeyError as exc:
            raise KeyError(
                f"unknown fortune provider: {name}"
            ) from exc
    def names(self) -> list[str]:
        return list(self._providers.keys())
    def infos(self) -> list[FortuneProviderInfo]:
        return list(self._info.values())
    def has(self, name: str) -> bool:
        return name.strip().lower() in self._providers
