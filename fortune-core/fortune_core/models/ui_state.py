from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class FortuneUiState:
    user_key: str
    theme: str = "general"
    active_system: str = "unified"
    active_page: str = "home"
    question: str = ""
    selected_result_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "user_key": self.user_key,
            "theme": self.theme,
            "active_system": self.active_system,
            "active_page": self.active_page,
            "question": self.question,
            "selected_result_id": self.selected_result_id,
            "metadata": self.metadata,
        }