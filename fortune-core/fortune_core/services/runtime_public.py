from __future__ import annotations
from typing import Any
class FortuneRuntimePublicService:
    """
    UI/frontend向けに内部実装詳細を隠した公開レスポンスを作る。
    """
    @staticmethod
    def response(result: dict[str, Any]) -> dict[str, Any]:
        return {
            "request_id": result.get("request_id"),
            "operation": result.get("operation"),
            "theme": result.get("theme"),
            "cached": result.get("cached", False),
            "result": result.get("result", {}),
        }
    @staticmethod
    def error(
        message: str,
        request_id: str | None = None,
    ) -> dict[str, Any]:
        return {
            "request_id": request_id,
            "success": False,
            "error": message,
        }