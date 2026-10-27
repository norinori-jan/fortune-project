from __future__ import annotations

import base64
import hashlib

from fortune_core.models.result_card import FortuneResultCard
from fortune_core.models.share_card import FortuneShareCard


class FortuneShareCardService:
    def build(
        self,
        card: FortuneResultCard,
    ) -> FortuneShareCard:
        seed = (
            f"{card.result_id}|"
            f"{card.theme}|"
            f"{card.headline}"
        )

        share_id = hashlib.sha256(
            seed.encode("utf-8")
        ).hexdigest()[:12]

        token = base64.urlsafe_b64encode(
            share_id.encode("utf-8")
        ).decode("ascii").rstrip("=")

        return FortuneShareCard(
            share_id=share_id,
            title="Fortune Hub",
            subtitle=f"{card.system} / {card.theme}",
            headline=card.headline,
            message=card.message,
            keywords=card.keywords,
            url_token=token,
            metadata={
                "system": card.system,
                "theme": card.theme,
            },
        )