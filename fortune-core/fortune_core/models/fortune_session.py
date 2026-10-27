from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass
class FortuneSession:
    session_id: str
    question: str
    system: str
    theme: str
    history_ids: list[str] = field(default_factory=list)
    favorite_ids: list[str] = field(default_factory=list)
    def add_history(self, record_id: str) -> None:
        if record_id not in self.history_ids:
            self.history_ids.append(record_id)
    def add_favorite(self, favorite_id: str) -> None:
        if favorite_id not in self.favorite_ids:
            self.favorite_ids.append(favorite_id)
    def to_dict(self) -> dict[str, Any]:
        return {
            "session_id": self.session_id,
            "question": self.question,
            "system": self.system,
            "theme": self.theme,
            "history_ids": list(self.history_ids),
            "favorite_ids": list(self.favorite_ids),
        }
