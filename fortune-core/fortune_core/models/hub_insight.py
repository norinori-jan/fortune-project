from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class HubInsight:
    key: str
    title: str
    message: str
    keywords: tuple[str, ...] = ()
    actions: tuple[str, ...] = ()
    metadata: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "message": self.message,
            "keywords": list(self.keywords),
            "actions": list(self.actions),
            "metadata": self.metadata,
        }
@dataclass(frozen=True)
class HubInsightCollection:
    theme: str
    insights: tuple[HubInsight, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "theme": self.theme,
            "insights": [
                insight.to_dict()
                for insight in self.insights
            ],
        }