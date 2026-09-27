from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class FortuneRuntimeUserState:
    user_key: str
    session_id: str | None = None
    theme: str = "general"
    last_request_id: str | None = None
    favorite_ids: tuple[str, ...] = ()
    recent_request_ids: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "session_id": self.session_id,
            "theme": self.theme,
            "last_request_id": self.last_request_id,
            "favorite_ids": list(self.favorite_ids),
            "recent_request_ids": list(self.recent_request_ids),
            "metadata": self.metadata,
        }
