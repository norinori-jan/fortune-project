from __future__ import annotations

from datetime import datetime, timezone

from fortune_core.models.runtime_export import FortuneRuntimeExport
from fortune_core.services.runtime_user import (
    FortuneRuntimeUserService,
)
from fortune_core.services.runtime_user_platform import (
    FortuneRuntimeUserPlatformService,
)


class FortuneRuntimeExportService:
    def __init__(
        self,
        user: FortuneRuntimeUserService | None = None,
        platform: FortuneRuntimeUserPlatformService | None = None,
    ) -> None:
        self.user = user or FortuneRuntimeUserService()
        self.platform = (
            platform
            or FortuneRuntimeUserPlatformService()
        )

    def export(
        self,
        user_key: str,
    ) -> FortuneRuntimeExport:
        user = self.platform.get_user(user_key)

        return FortuneRuntimeExport(
            user_key=user_key,
            generated_at=datetime.now(
                timezone.utc
            ).isoformat(),
            profile=self.user.profile(user_key),
            summary=self.user.summary_for(user_key),
            preferences=user["preferences"],
            usage=user["usage"],
            notifications=user["notifications"],
            recommendations=tuple(
                self.user.recommendations_for(user_key)
            ),
        )