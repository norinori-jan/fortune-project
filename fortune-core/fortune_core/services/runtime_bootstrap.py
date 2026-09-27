from __future__ import annotations

from fortune_core.models.runtime_bootstrap import (
    FortuneRuntimeBootstrap,
)
from fortune_core.services.runtime_contract import (
    FortuneRuntimeContractService,
)
from fortune_core.services.runtime_features import (
    FortuneRuntimeFeatureService,
)
from fortune_core.services.runtime_user import (
    FortuneRuntimeUserService,
)
from fortune_core.services.runtime_user_platform import (
    FortuneRuntimeUserPlatformService,
)
from fortune_core.services.runtime_daily import (
    FortuneRuntimeDailyService,
)


class FortuneRuntimeBootstrapService:
    def __init__(self) -> None:
        self.user = FortuneRuntimeUserService()
        self.platform = FortuneRuntimeUserPlatformService()
        self.features = FortuneRuntimeFeatureService()
        self.contract = FortuneRuntimeContractService()
        self.daily = FortuneRuntimeDailyService()

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> FortuneRuntimeBootstrap:
        platform = self.platform.get_user(user_key)

        return FortuneRuntimeBootstrap(
            service="fortune-hub",
            version="1.0.0",
            user_key=user_key,
            theme=theme,
            daily=self.daily.get(
                user_key=user_key,
                theme=theme,
            ).to_dict(),
            profile=self.user.profile(user_key),
            preferences=platform["preferences"],
            recommendations=tuple(
                self.user.recommendations_for(
                    user_key,
                    themes=[theme],
                )
            ),
            features=tuple(
                self.features_item.to_dict()
                for self.features_item
                in self.features.list()
            ),
            contract=self.contract.get().to_dict(),
        )