from __future__ import annotations
from dataclasses import dataclass
from typing import Any
from .fortune_provider_result import FortuneProviderResult
@dataclass(frozen=True)
class FortuneBatchResult:
    theme: str
    question: str
    requested_providers: tuple[str, ...]
    results: tuple[FortuneProviderResult, ...]
    @property
    def success_count(self) -> int:
        return sum(
            1
            for result in self.results
            if result.success
        )
    @property
    def failure_count(self) -> int:
        return len(self.results) - self.success_count
    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "question": self.question,
            "requested_providers": list(
                self.requested_providers
            ),
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "results": [
                result.to_dict()
                for result in self.results
            ],
        }