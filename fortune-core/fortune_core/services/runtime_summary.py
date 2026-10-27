from __future__ import annotations
from fortune_core.models.runtime_summary import FortuneRuntimeSummary
from fortune_core.services.runtime_history import (
    FortuneRuntimeHistoryService,
)
class FortuneRuntimeSummaryService:
    def __init__(
        self,
        history: FortuneRuntimeHistoryService | None = None,
    ) -> None:
        self.history = history or FortuneRuntimeHistoryService()
    def summarize(
        self,
        user_key: str,
    ) -> FortuneRuntimeSummary:
        records = self.history.list(user_key=user_key)
        themes = tuple(dict.fromkeys(
            item.theme for item in records
        ))
        operations = tuple(dict.fromkeys(
            item.operation for item in records
        ))
        latest = records[-1] if records else None
        return FortuneRuntimeSummary(
            user_key=user_key,
            total_requests=len(records),
            successful_requests=sum(
                1 for item in records
                if item.success
            ),
            cached_requests=sum(
                1 for item in records
                if item.cached
            ),
            themes=themes,
            operations=operations,
            latest_request_id=(
                latest.request_id
                if latest is not None
                else None
            ),
            latest_theme=(
                latest.theme
                if latest is not None
                else None
            ),
        )