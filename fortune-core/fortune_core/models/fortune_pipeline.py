from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
from .fortune_context import FortuneContext
from .fortune_result import FortuneResult
from .fortune_score import FortuneScore
from .cross_summary import CrossSummary
@dataclass(frozen=True)
class FortunePipelineResult:
    context: FortuneContext
    results: tuple[FortuneResult, ...]
    scores: tuple[FortuneScore, ...]
    summary: CrossSummary
    execution_id: str
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "context": self.context.to_dict(),
            "results": [
                result.to_dict()
                for result in self.results
            ],
            "scores": [
                score.to_dict()
                for score in self.scores
            ],
            "summary": self.summary.to_dict(),
            "execution_id": self.execution_id,
            "metadata": dict(self.metadata),
        }
