from __future__ import annotations

from typing import Any

from fortune_core.services.screen_home import (
    FortuneHomeScreenService,
)
from fortune_core.services.screen_today import (
    FortuneTodayScreenService,
)
from fortune_core.services.screen_question import (
    FortuneQuestionScreenService,
)


class FortuneMobileShellService:
    def __init__(self) -> None:
        self.home = FortuneHomeScreenService()
        self.today = FortuneTodayScreenService()
        self.question = FortuneQuestionScreenService()

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> dict[str, Any]:
        return {
            "app": "fortune-hub",
            "navigation_mode": "bottom-tabs",
            "screens": {
                "home": self.home.build(
                    user_key=user_key,
                    theme=theme,
                ),
                "today": self.today.build(
                    user_key=user_key,
                    theme=theme,
                ),
                "question": self.question.build(
                    theme=theme,
                ),
            },
            "metadata": {
                "platform": "mobile",
                "version": "1.0.0",
            },
        }