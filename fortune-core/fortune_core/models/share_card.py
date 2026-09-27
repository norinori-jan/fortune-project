from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneShareCard:
    share_id: str
    title: str
    subtitle: str
    headline: str
    message: str
    keywords: tuple[str, ...]
    url_token: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "share_id": self.share_id,
            "title": self.title,
            "subtitle": self.subtitle,
            "headline": self.headline,
            "message": self.message,
            "keywords": list(self.keywords),
            "url_token": self.url_token,
            "metadata": self.metadata,
        }