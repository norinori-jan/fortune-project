from __future__ import annotations

from fortune_core.models.runtime_platform import (
    FortuneRuntimePlatformSnapshot,
)
from fortune_core.services.runtime_config import (
    FortuneRuntimeConfigService,
)
from fortune_core.services.runtime_user_platform import (
    FortuneRuntimeUserPlatformService,
)


class FortuneRuntimePlatformService:
    def __init__(
        self,
        users: FortuneRuntimeUserPlatformService | None = None,
        config: FortuneRuntimeConfigService | None = None,
    ) -> None:
        self.users = (
            users
            or FortuneRuntimeUserPlatformService()
        )
        self.config = (
            config
            or FortuneRuntimeConfigService()
        )

    def snapshot(
        self,
        user_key: str,
    ) -> FortuneRuntimePlatformSnapshot:
        user = self.users.get_user(user_key)

        return FortuneRuntimePlatformSnapshot(
            service=self.config.get().service_name,
            version=self.config.get().version,
            user_key=user_key,
            preferences=user["preferences"],
            usage=user["usage"],
            notifications=user["notifications"],
            features=tuple(
                self.users.features_snapshot()
            ),
        )