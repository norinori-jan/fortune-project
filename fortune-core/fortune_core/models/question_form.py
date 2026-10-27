from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneQuestionForm:
    theme: str
    placeholder: str
    examples: tuple[str, ...]
    min_length: int
    max_length: int
    submit_label: str
    metadata: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "placeholder": self.placeholder,
            "examples": list(self.examples),
            "min_length": self.min_length,
            "max_length": self.max_length,
            "submit_label": self.submit_label,
            "metadata": self.metadata,
        }