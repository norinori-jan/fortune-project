from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneFavoritesView:
    user_key: str
    items: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "items": list(self.items),
            "count": len(self.items),
        }