from __future__ import annotations

from typing import Any

from fortune_core.models.result_screen import (
    FortuneResultScreen,
)
from fortune_core.services.result_card import (
    FortuneResultCardService,
)
from fortune_core.services.share_card import (
    FortuneShareCardService,
)
from fortune_core.services.ui_actions import (
    FortuneUiActionService,
)


class FortuneResultScreenService:
    def __init__(self) -> None:
        self.cards = FortuneResultCardService()
        self.share = FortuneShareCardService()
        self.actions = FortuneUiActionService()

    def build(
        self,
        system: str,
        theme: str,
        result: dict[str, Any],
    ) -> FortuneResultScreen:
        card = self.cards.build(
            system=system,
            theme=theme,
            result=result,
        )

        share = self.share.build(card)

        actions = (
            self.actions.home_actions(theme)
        )

        return FortuneResultScreen(
            result=result,
            card=card.to_dict(),
            share=share.to_dict(),
            actions=tuple(
                item.to_dict()
                for item in actions
            ),
            metadata={
                "screen": "result",
                "result_id": card.result_id,
            },
        )