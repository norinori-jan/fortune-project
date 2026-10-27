from __future__ import annotations

from fortune_core.models.runtime_overview import (
    FortuneRuntimeOverview,
)
from fortune_core.services.runtime_contract import (
    FortuneRuntimeContractService,
)
from fortune_core.services.runtime_discovery import (
    FortuneRuntimeDiscoveryService,
)
from fortune_core.services.runtime_features import (
    FortuneRuntimeFeatureService,
)
from fortune_core.services.runtime_help import (
    FortuneRuntimeHelpService,
)


class FortuneRuntimeOverviewService:
    def __init__(self) -> None:
        self.contract = FortuneRuntimeContractService()
        self.discovery = FortuneRuntimeDiscoveryService()
        self.features = FortuneRuntimeFeatureService()
        self.help = FortuneRuntimeHelpService()

    def get(self) -> FortuneRuntimeOverview:
        return FortuneRuntimeOverview(
            contract=self.contract.get().to_dict(),
            discovery=tuple(
                item.to_dict()
                for item in self.discovery.list()
            ),
            help_items=tuple(
                item.to_dict()
                for item in self.help.list()
            ),
            features=tuple(
                item.to_dict()
                for item in self.features.list()
            ),
        )