from __future__ import annotations
import hashlib
from datetime import date
from typing import Any
from ..models.fortune_context import FortuneContext
from ..models.fortune_pipeline import FortunePipelineResult
from ..models.fortune_result import FortuneResult
from .context import FortuneContextService
from .result_normalizer import FortuneResultNormalizer
from .fortune_scoring import FortuneScoringService
from .cross_summary import FortuneCrossSummaryService
from .complete_fortune import CompleteFortuneService
class FortunePipelineService:
    """
    Hub の標準実行パイプライン。
    1. Context生成
    2. 占術実行
    3. 共通Resultへ正規化
    4. スコア情報生成
    5. 横断サマリー生成
    """
    def __init__(self) -> None:
        self.context_service = FortuneContextService()
        self.normalizer = FortuneResultNormalizer()
        self.scoring = FortuneScoringService()
        self.cross_summary = FortuneCrossSummaryService()
        self.complete_service = CompleteFortuneService()
    def execute(
        self,
        *,
        user_key: str | None = None,
        birth_date: str | None = None,
        question: str = "",
        theme: str = "general",
        today: date | None = None,
    ) -> FortunePipelineResult:
        context = self.context_service.create(
            user_key=user_key,
            birth_date=birth_date,
            question=question,
            theme=theme,
        )
        raw = self.complete_service.divine(
            question=context.question,
            theme=context.theme,
        )
        normalized = self._normalize_complete(
            context=context,
            raw=raw,
        )
        scores = tuple(
            self.scoring.score(
                system=result.system,
                theme=context.theme,
                question=context.question,
            )
            for result in normalized
        )
        enriched = tuple(
            self._apply_score(
                result=result,
                score=score,
            )
            for result, score in zip(normalized, scores)
        )
        summary = self.cross_summary.summarize(
            theme=context.theme,
            results=enriched,
        )
        execution_id = self._execution_id(
            context=context,
            today=today or date.today(),
        )
        return FortunePipelineResult(
            context=context,
            results=enriched,
            scores=scores,
            summary=summary,
            execution_id=execution_id,
            metadata={
                "date": (today or date.today()).isoformat(),
                "pipeline_version": "1",
            },
        )
    def _normalize_complete(
        self,
        *,
        context: FortuneContext,
        raw: Any,
    ) -> tuple[FortuneResult, ...]:
        results: list[FortuneResult] = []
        raw_data = self._as_dict(raw)
        for system in ("unified", "tarot", "meihua"):
            if system not in raw_data:
                continue
            result = self.normalizer.normalize(
                system=system,
                theme=context.theme,
                result=raw_data[system],
            )
            results.append(result)
        return tuple(results)
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
        return {}
    @staticmethod
    def _apply_score(
        *,
        result: FortuneResult,
        score: Any,
    ) -> FortuneResult:
        return FortuneResult(
            result_id=result.result_id,
            system=result.system,
            theme=result.theme,
            title=result.title,
            summary=result.summary,
            message=result.message,
            keywords=result.keywords,
            score=score.score,
            metadata={
                **result.metadata,
                "score_label": score.label,
            },
        )
    @staticmethod
    def _execution_id(
        *,
        context: FortuneContext,
        today: date,
    ) -> str:
        raw = (
            f"{context.user_key}|"
            f"{context.birth_date}|"
            f"{context.question}|"
            f"{context.theme}|"
            f"{today.isoformat()}"
        )
        digest = hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()
        return f"exec-{digest[:20]}"