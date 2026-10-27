from __future__ import annotations

from fortune_core.services.question_guide import (
    FortuneQuestionGuideService,
)
from fortune_core.models.question_form import (
    FortuneQuestionForm,
)


class FortuneQuestionFormService:
    def __init__(self) -> None:
        self.guides = FortuneQuestionGuideService()

    def build(
        self,
        theme: str = "general",
    ) -> FortuneQuestionForm:
        guide = self.guides.get(theme)

        return FortuneQuestionForm(
            theme=guide.theme,
            placeholder=(
                "今気になっていることを"
                "自由に入力してください"
            ),
            examples=guide.examples,
            min_length=1,
            max_length=500,
            submit_label="占ってみる",
            metadata={
                "recommended_systems": list(
                    guide.recommended_systems
                ),
                "tips": list(guide.tips),
            },
        )
