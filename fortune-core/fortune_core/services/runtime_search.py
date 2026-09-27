from __future__ import annotations

from fortune_core.models.runtime_search import (
    FortuneRuntimeSearchResult,
)
from fortune_core.services.runtime_discovery import (
    FortuneRuntimeDiscoveryService,
)
from fortune_core.services.runtime_help import (
    FortuneRuntimeHelpService,
)


class FortuneRuntimeSearchService:
    def __init__(self) -> None:
        self.discovery = FortuneRuntimeDiscoveryService()
        self.help = FortuneRuntimeHelpService()

    def search(
        self,
        query: str,
    ) -> list[FortuneRuntimeSearchResult]:
        normalized = query.strip().lower()

        if not normalized:
            return []

        results: list[FortuneRuntimeSearchResult] = []

        for item in self.discovery.list():
            haystack = " ".join(
                (
                    item.key,
                    item.title,
                    item.description,
                    item.theme,
                    *item.keywords,
                )
            ).lower()

            if normalized not in haystack:
                continue

            score = 1.0

            if normalized == item.key.lower():
                score += 2.0

            if normalized in item.title.lower():
                score += 1.0

            results.append(
                FortuneRuntimeSearchResult(
                    key=item.key,
                    title=item.title,
                    category=item.category,
                    score=score,
                    metadata=item.to_dict(),
                )
            )

        for item in self.help.list():
            haystack = " ".join(
                (
                    item.key,
                    item.title,
                    item.description,
                    item.example_question,
                    *item.keywords,
                )
            ).lower()

            if normalized not in haystack:
                continue

            results.append(
                FortuneRuntimeSearchResult(
                    key=f"help:{item.key}",
                    title=item.title,
                    category="help",
                    score=0.8,
                    metadata=item.to_dict(),
                )
            )

        return sorted(
            results,
            key=lambda item: item.score,
            reverse=True,
        )