from __future__ import annotations
from collections import Counter
from ..models.fortune_comparison_run import FortuneComparisonRun
from .fortune_batch import FortuneBatchService
class FortuneComparisonRunService:
    def __init__(self) -> None:
        self.batch = FortuneBatchService()
    def execute(
        self,
        *,
        question: str = "",
        theme: str = "general",
        providers: tuple[str, ...] | None = None,
    ) -> FortuneComparisonRun:
        result = self.batch.execute(
            question=question,
            theme=theme,
            providers=providers,
        )
        keywords: Counter[str] = Counter()
        for item in result.results:
            raw = item.result.get("keywords", [])
            if isinstance(raw, str):
                keywords[raw] += 1
            elif isinstance(raw, list):
                keywords.update(
                    str(value)
                    for value in raw
                )
        common = tuple(
            keyword
            for keyword, _ in keywords.most_common(5)
        )
        return FortuneComparisonRun(
            theme=theme,
            question=question,
            items=result.results,
            common_keywords=common,
        )