from __future__ import annotations
from typing import Any
from fortune_core.services.runtime_capabilities import (
    FortuneRuntimeCapabilityService,
)
from fortune_core.services.service_manifest import (
    FortuneServiceManifestService,
)
from fortune_core.services.theme_router import (
    FortuneThemeRouterService,
)
class FortuneRuntimeCatalogService:
    def __init__(
        self,
        manifests: FortuneServiceManifestService | None = None,
        capabilities: FortuneRuntimeCapabilityService | None = None,
        themes: FortuneThemeRouterService | None = None,
    ) -> None:
        self.manifests = (
            manifests
            or FortuneServiceManifestService()
        )
        self.capabilities = (
            capabilities
            or FortuneRuntimeCapabilityService()
        )
        self.themes = (
            themes
            or FortuneThemeRouterService()
        )
    def catalog(self) -> dict[str, Any]:
        return {
            "service": "fortune-runtime",
            "version": "1.0.0",
            "services": [
                item.to_dict()
                for item in self.manifests.list()
            ],
            "capabilities": [
                item.to_dict()
                for item in self.capabilities.list()
            ],
            "themes": [
                item.to_dict()
                for item in self.themes.list()
            ],
        }