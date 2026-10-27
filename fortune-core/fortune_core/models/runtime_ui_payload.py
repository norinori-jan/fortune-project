from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneRuntimeUiPayload:
    user_key: str
    theme: str
    page: dict[str, Any]
    daily: dict[str, Any]
    question_guide: dict[str, Any]
    recommendations: tuple[dict[str, Any], ...]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "theme": self.theme,
            "page": self.page,
            "daily": self.daily,
            "question_guide": self.question_guide,
            "recommendations": list(self.recommendations),
            "metadata": self.metadata,
        }