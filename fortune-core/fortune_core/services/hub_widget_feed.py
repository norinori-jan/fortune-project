from __future__ import annotations

from typing import Any

from fortune_core.services.hub_page import (
    FortuneHubPageService,
)
from fortune_core.services.question_guide import (
    FortuneQuestionGuideService,
)


class FortuneHubWidgetFeedService:
    def __init__(self) -> None:
        self.page = FortuneHubPageService()
        self.questions = FortuneQuestionGuideService()

    def build(
        self,
        user_key: str,
        theme: str = "general",
    ) -> dict[str, Any]:
        page = self.page.home(
            user_key=user_key,
            theme=theme,
        )

        guide = self.questions.get(theme)

        return {
            "page": page.to_dict(),
            "question_guide": guide.to_dict(),
            "ui": {
                "layout": "fortune-hub",
                "theme": theme,
                "version": "1.0",
            },
        }
