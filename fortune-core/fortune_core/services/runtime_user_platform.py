from __future__ import annotations

from typing import Any

from fortune_core.services.runtime_features import (
    FortuneRuntimeFeatureService,
)
from fortune_core.services.runtime_notifications import (
    FortuneRuntimeNotificationService,
)
from fortune_core.services.runtime_preferences import (
    FortuneRuntimePreferencesService,
)
from fortune_core.services.runtime_usage import (
    FortuneRuntimeUsageService,
)


class FortuneRuntimeUserPlatformService:
    def __init__(self) -> None:
        self.preferences = FortuneRuntimePreferencesService()
        self.features = FortuneRuntimeFeatureService()
        self.usage = FortuneRuntimeUsageService()
        self.notifications = FortuneRuntimeNotificationService()

    def get_user(
        self,
        user_key: str,
    ) -> dict[str, Any]:
        return {
            "preferences": self.preferences.get(
                user_key
            ).to_dict(),
            "usage": self.usage.get(
                user_key
            ).to_dict(),
            "notifications": self.notifications.get(
                user_key
            ).to_dict(),
        }

    def features_snapshot(self) -> list[dict[str, Any]]:
        return [
            item.to_dict()
            for item in self.features.list()
        ]