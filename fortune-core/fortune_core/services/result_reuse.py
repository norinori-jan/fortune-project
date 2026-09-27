from __future__ import annotations

from typing import Any

from fortune_core.models.result_reuse import FortuneResultReuse


class FortuneResultReuseService:
    def build_from_history(
        self,
        item: dict[str, Any],
    ) -> FortuneResultReuse:
        return FortuneResultReuse(
            source_id=str(
                item.get("request_id", "")
            ),
            title=(
                item.get("title")
                or f"{item.get('theme', 'general')}の占い結果"
            ),
            question=str(
                item.get("question", "")
            ),
            theme=str(
                item.get("theme", "general")
            ),
            system=str(
                item.get("system", "unified")
            ),
            result=dict(
                item.get("result", {})
            ),
        )

    def build_question(
        self,
        item: FortuneResultReuse,
    ) -> str:
        return item.question