from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass
class FortuneHubState:
    user_key: str
    theme: str = "general"
    last_question: str = ""
    last_result_id: str | None = None
    favorite_ids: list[str] = field(default_factory=list)
    history_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    def remember_result(self, result_id: str) -> None:
        self.last_result_id = result_id
        if result_id not in self.history_ids:
            self.history_ids.append(result_id)
    def add_favorite(self, result_id: str) -> None:
        if result_id not in self.favorite_ids:
            self.favorite_ids.append(result_id)
    def remove_favorite(self, result_id: str) -> None:
        if result_id in self.favorite_ids:
            self.favorite_ids.remove(result_id)
    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "theme": self.theme,
            "last_question": self.last_question,
            "last_result_id": self.last_result_id,
            "favorite_ids": list(self.favorite_ids),
            "history_ids": list(self.history_ids),
            "metadata": dict(self.metadata),
        }