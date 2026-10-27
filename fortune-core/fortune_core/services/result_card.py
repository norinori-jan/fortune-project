from __future__ import annotations

import hashlib
from typing import Any

from fortune_core.models.result_card import FortuneResultCard


class FortuneResultCardService:
    def build(
        self,
        system: str,
        theme: str,
        result: dict[str, Any],
    ) -> FortuneResultCard:
        raw = (
            f"{system}|{theme}|"
            f"{result.get('question', '')}|"
            f"{result.get('message', '')}"
        )
        result_id = hashlib.sha256(
            raw.encode("utf-8")
        ).hexdigest()[:16]

        score = result.get("score")

        keywords = result.get("keywords", ())
        if isinstance(keywords, str):
            keywords = (keywords,)

        headline = (
            result.get("headline")
            or result.get("title")
            or f"{theme}のメッセージ"
        )

        message = (
            result.get("message")
            or result.get("summary")
            or result.get("overall")
            or ""
        )

        advice = (
            result.get("advice")
            or result.get("recommendation")
            or ""
        )

        return FortuneResultCard(
            result_id=result_id,
            title=f"{system}・{theme}",
            system=system,
            theme=theme,
            headline=str(headline),
            score=int(score) if score is not None else None,
            message=str(message),
            advice=str(advice),
            keywords=tuple(str(x) for x in keywords),
            metadata={
                "source": "fortune-result-card",
            },
        )