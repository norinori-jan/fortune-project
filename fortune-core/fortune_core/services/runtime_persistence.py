from __future__ import annotations

from typing import Any

from fortune_core.services.runtime_repository import (
    FortuneRuntimeRepository,
    InMemoryFortuneRuntimeRepository,
)


class FortuneRuntimePersistenceService:
    """
    永続化方式をInMemoryから外部DB等へ差し替えるための薄い層。
    """

    def __init__(
        self,
        repository: FortuneRuntimeRepository | None = None,
    ) -> None:
        self.repository = (
            repository
            or InMemoryFortuneRuntimeRepository()
        )

    def put(
        self,
        key: str,
        value: dict[str, Any],
    ) -> dict[str, Any]:
        self.repository.save(key, value)
        return value

    def get(
        self,
        key: str,
    ) -> dict[str, Any] | None:
        return self.repository.get(key)

    def delete(self, key: str) -> bool:
        return self.repository.delete(key)

    def all(self) -> list[dict[str, Any]]:
        return self.repository.list()