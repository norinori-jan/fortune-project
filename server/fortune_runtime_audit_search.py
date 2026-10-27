from __future__ import annotations

from fastapi import APIRouter

from fortune_core.services.runtime_audit_search import (
    FortuneRuntimeAuditSearchService,
)


router = APIRouter(
    prefix="/fortune/audit-search",
    tags=["fortune-audit"],
)

_service = FortuneRuntimeAuditSearchService()


@router.get("")
def audit_search(
    user_key: str | None = None,
    operation: str | None = None,
    theme: str | None = None,
    limit: int = 50,
) -> list[dict]:
    return _service.search(
        user_key=user_key,
        operation=operation,
        theme=theme,
        limit=limit,
    )