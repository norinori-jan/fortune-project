from __future__ import annotations
import hashlib
from typing import Any
from ..models.fortune_result import FortuneResult
class FortuneResultNormalizer:
    """
    異なる占術サービスの戻り値をHub共通形式へ正規化する。
    """
    def normalize(
        self,
        *,
        system: str,
        theme: str,
        result: Any,
        title: str | None = None,
    ) -> FortuneResult:
        data = self._as_dict(result)
        result_id = self._make_id(
            system=system,
            theme=theme,
            data=data,
        )
        resolved_title = (
            title
            or self._first_text(
                data,
                "title",
                "name",
                "card",
                "hexagram",
                default=system,
            )
        )
        summary = self._first_text(
            data,
            "summary",
            "overall",
            "description",
            "message",
            default="",
        )
        message = self._first_text(
            data,
            "message",
            "advice",
            "interpretation",
            "summary",
            default=summary,
        )
        keywords = self._keywords(data)
        score = self._score(data)
        return FortuneResult(
            result_id=result_id,
            system=system,
            theme=theme,
            title=resolved_title,
            summary=summary,
            message=message,
            keywords=tuple(keywords),
            score=score,
            metadata={
                "source_keys": sorted(data.keys()),
            },
        )
    @staticmethod
    def _as_dict(value: Any) -> dict[str, Any]:
        if isinstance(value, dict):
            return value
        if hasattr(value, "to_dict"):
            converted = value.to_dict()
            if isinstance(converted, dict):
                return converted
        if hasattr(value, "__dict__"):
            return dict(value.__dict__)
        return {"value": value}
    @staticmethod
    def _first_text(
        data: dict[str, Any],
        *keys: str,
        default: str = "",
    ) -> str:
        for key in keys:
            value = data.get(key)
            if value is None:
                continue
            if isinstance(value, str) and value.strip():
                return value.strip()
            if isinstance(value, (int, float)):
                return str(value)
        return default
    @staticmethod
    def _keywords(data: dict[str, Any]) -> list[str]:
        raw = data.get("keywords", [])
        if isinstance(raw, str):
            return [raw]
        if isinstance(raw, (list, tuple, set)):
            return [
                str(item)
                for item in raw
                if str(item).strip()
            ]
        return []
    @staticmethod
    def _score(data: dict[str, Any]) -> int | None:
        for key in ("score", "rating", "fortune_score"):
            value = data.get(key)
            if isinstance(value, (int, float)):
                return int(value)
        return None
    @staticmethod
    def _make_id(
        *,
        system: str,
        theme: str,
        data: dict[str, Any],
    ) -> str:
        raw = (
            f"{system}|{theme}|"
            f"{sorted(data.items(), key=lambda item: item[0])}"
        )
        digest = hashlib.sha256(
            raw.encode("utf-8", errors="replace")
        ).hexdigest()
        return f"{system}-{digest[:16]}"