from __future__ import annotations
from typing import Any
from fortune_core.models.hub_runtime import HubRuntimeRequest
from fortune_core.services.runtime_catalog import (
    FortuneRuntimeCatalogService,
)
from fortune_core.services.runtime_user import (
    FortuneRuntimeUserService,
)
class FortuneRuntimeIntegrationService:
    """
    UI / API側が1つのサービスだけを利用すればよい統合入口。
    """
    def __init__(
        self,
        user_service: FortuneRuntimeUserService | None = None,
        catalog: FortuneRuntimeCatalogService | None = None,
    ) -> None:
        self.user_service = (
            user_service
            or FortuneRuntimeUserService()
        )
        self.catalog_service = (
            catalog
            or FortuneRuntimeCatalogService()
        )
    def execute(
        self,
        request: HubRuntimeRequest,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        return self.user_service.execute(
            request,
            session_id=session_id,
        )
    def home(
        self,
        user_key: str,
        theme: str = "general",
        session_id: str | None = None,
    ) -> dict[str, Any]:
        return self.execute(
            HubRuntimeRequest(
                user_key=user_key,
                theme=theme,
                operation="home",
            ),
            session_id=session_id,
        )
    def quick(
        self,
        user_key: str,
        question: str,
        theme: str = "general",
        session_id: str | None = None,
    ) -> dict[str, Any]:
        return self.execute(
            HubRuntimeRequest(
                user_key=user_key,
                question=question,
                theme=theme,
                operation="quick",
            ),
            session_id=session_id,
        )
    def today(
        self,
        user_key: str,
        theme: str = "general",
        session_id: str | None = None,
    ) -> dict[str, Any]:
        return self.execute(
            HubRuntimeRequest(
                user_key=user_key,
                theme=theme,
                operation="today",
            ),
            session_id=session_id,
        )
    def catalog(self) -> dict[str, Any]:
        return self.catalog_service.catalog()