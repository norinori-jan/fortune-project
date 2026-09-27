from __future__ import annotations

from typing import Any

from fortune_core.services.runtime_bootstrap import (
    FortuneRuntimeBootstrapService,
)
from fortune_core.services.runtime_feed import (
    FortuneRuntimeFeedService,
)


class FortuneRuntimePublicFeedService:
    def __init__(self) -> None:
        self.bootstrap = FortuneRuntimeBootstrapService()
        self.feed = FortuneRuntimeFeedService()

    def home(
        self,
        user_key: str,
        theme: str = "general",
    ) -> dict[str, Any]:
        return {
            "bootstrap": self.bootstrap.build(
                user_key=user_key,
                theme=theme,
            ).to_dict(),
            "feed": self.feed.build(
                user_key=user_key,
                theme=theme,
            ),
        }