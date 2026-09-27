from __future__ import annotations

from typing import Any

from fortune_core.services.hub_page import (
    FortuneHubPageService,
)
from fortune_core.services.theme_ui import (
    FortuneThemeUiService,
)
from fortune_core.services.ui_state import (
    FortuneUiStateService,
)


class FortuneUiShellService:
    def __init__(self) -> None:
        self.page = FortuneHubPageService()
        self.theme = FortuneThemeUiService()
        self.state = FortuneUiStateService()

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> dict[str, Any]:
        self.state.set_theme(
            user_key=user_key,
            theme=theme,
        )

        return {
            "state": self.state.get(
                user_key
            ).to_dict(),
            "page": self.page.home(
                user_key=user_key,
                theme=theme,
            ).to_dict(),
            "theme": self.theme.build(theme),
            "metadata": {
                "surface": "fortune-hub",
                "shell_version": "1.0.0",
            },
        }