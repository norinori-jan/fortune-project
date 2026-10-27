from __future__ import annotations

from typing import Any, Protocol


class FortuneRuntimeRepository(Protocol):
    def save(
        self,
        key: str,
        value: dict[str, Any],
    ) -> None:
        ...

    def get(
        self,
        key: str,
    ) -> dict[str, Any] | None:
        ...

    def delete(
        self,
        key: str,
    ) -> bool:
        ...

    def list(self) -> list[dict[str, Any]]:
        ...


class InMemoryFortuneRuntimeRepository:
    def __init__(self) -> None:
        self._items: dict[str, dict[str, Any]] = {}

    def save(
        self,
        key: str,
        value: dict[str, Any],
    ) -> None:
        self._items[key] = dict(value)

    def get(
        self,
        key: str,
    ) -> dict[str, Any] | None:
        value = self._items.get(key)

        if value is None:
            return None

        return dict(value)

    def delete(self, key: str) -> bool:
        return self._items.pop(key, None) is not None

    def list(self) -> list[dict[str, Any]]:
        return [
            dict(item)
            for item in self._items.values()
        ]