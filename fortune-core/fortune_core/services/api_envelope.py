from __future__ import annotations
from typing import Any
from ..models.fortune_api_envelope import FortuneApiEnvelope
from .response_meta import FortuneResponseMetaService
class FortuneApiEnvelopeService:
    def __init__(self) -> None:
        self.meta = FortuneResponseMetaService()
    def success(
        self,
        *,
        data: Any,
        question: str,
        theme: str,
        system_count: int = 0,
    ) -> FortuneApiEnvelope:
        metadata = self.meta.create(
            question=question,
            theme=theme,
            system_count=system_count,
        )
        if hasattr(data, "to_dict"):
            payload = data.to_dict()
        else:
            payload = data
        return FortuneApiEnvelope(
            ok=True,
            meta=metadata.to_dict(),
            data=payload,
        )
    def failure(
        self,
        *,
        error: str,
        question: str = "",
        theme: str = "general",
    ) -> FortuneApiEnvelope:
        metadata = self.meta.create(
            question=question,
            theme=theme,
            system_count=0,
        )
        return FortuneApiEnvelope(
            ok=False,
            meta=metadata.to_dict(),
            data=None,
            errors=(error,),
        )
