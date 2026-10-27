from __future__ import annotations

from typing import Any

from fortune_core.services.runtime_audit import (
    FortuneRuntimeAuditService,
)


class FortuneRuntimeAuditSearchService:
    def __init__(
        self,
        audit: FortuneRuntimeAuditService | None = None,
    ) -> None:
        self.audit = audit or FortuneRuntimeAuditService()

    def search(
        self,
        user_key: str | None = None,
        operation: str | None = None,
        theme: str | None = None,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        items = self.audit.list()

        if user_key is not None:
            items = [
                item
                for item in items
                if item.user_key == user_key
            ]

        if operation is not None:
            items = [
                item
                for item in items
                if item.operation == operation
            ]

        if theme is not None:
            items = [
                item
                for item in items
                if item.theme == theme
            ]

        items = items[-max(1, limit):]

        return [
            item.to_dict()
            for item in items
        ]