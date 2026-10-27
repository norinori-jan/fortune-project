from __future__ import annotations

from fortune_core.models.runtime_contract import (
    FortuneRuntimeContract,
)
from fortune_core.services.runtime_catalog import (
    FortuneRuntimeCatalogService,
)
from fortune_core.services.runtime_features import (
    FortuneRuntimeFeatureService,
)


class FortuneRuntimeContractService:
    def __init__(
        self,
        catalog: FortuneRuntimeCatalogService | None = None,
        features: FortuneRuntimeFeatureService | None = None,
    ) -> None:
        self.catalog = (
            catalog
            or FortuneRuntimeCatalogService()
        )
        self.features = (
            features
            or FortuneRuntimeFeatureService()
        )

    def get(self) -> FortuneRuntimeContract:
        catalog = self.catalog.catalog()

        systems = tuple(
            (item.get("name") or item.get("key"))
            for item in catalog.get("systems", [])
            if isinstance(item, dict)
        )

        themes = tuple(
            (item.get("name") or item.get("key"))
            for item in catalog.get("themes", [])
            if isinstance(item, dict)
        )

        features = tuple(
            item.name
            for item in self.features.list()
            if item.enabled
        )

        return FortuneRuntimeContract(
            name="fortune-hub-runtime",
            version="1.0.0",
            operations=(
                "home",
                "quick",
                "today",
                "execute",
            ),
            themes=themes,
            systems=systems,
            features=features,
        )