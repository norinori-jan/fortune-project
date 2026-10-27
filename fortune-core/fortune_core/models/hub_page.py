from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneHubPage:
    page_key: str
    title: str
    theme: str
    widgets: tuple[dict[str, Any], ...]
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "page_key": self.page_key,
            "title": self.title,
            "theme": self.theme,
            "widgets": list(self.widgets),
            "metadata": self.metadata,
        }