from __future__ import annotations

from typing import Any

from fortune_core.services.question_form import (
    FortuneQuestionFormService,
)
from fortune_core.services.system_selector import (
    FortuneSystemSelectorService,
)
from fortune_core.services.theme_tabs import (
    FortuneThemeTabService,
)
from fortune_core.services.ui_navigation import (
    FortuneUiNavigationService,
)


class FortuneQuestionScreenService:
    def __init__(self) -> None:
        self.form = FortuneQuestionFormService()
        self.systems = FortuneSystemSelectorService()
        self.navigation = FortuneUiNavigationService()
        self.themes = FortuneThemeTabService()

    def build(
        self,
        theme: str = "general",
    ) -> dict[str, Any]:
        return {
            "screen": "question",
            "navigation": [
                item.to_dict()
                for item in self.navigation.build("question")
            ],
            "themes": [
                item.to_dict()
                for item in self.themes.build(theme)
            ],
            "form": self.form.build(
                theme
            ).to_dict(),
            "systems": [
                item.to_dict()
                for item in self.systems.list(theme)
            ],
        }