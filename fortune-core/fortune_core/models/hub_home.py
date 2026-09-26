from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any
@dataclass(frozen=True)
class HubSection:
    key: str
    title: str
    summary: str
    data: dict[str, Any] = field(default_factory=dict)
    def to_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "title": self.title,
            "summary": self.summary,
            "data": self.data,
        }
@dataclass(frozen=True)
class FortuneHubHome:
    question: str
    theme: str
    profile: dict[str, Any]
    daily_message: dict[str, Any]
    dashboard: dict[str, Any]
    guidance: dict[str, Any]
    suggestions: list[dict[str, Any]]
    calendar: dict[str, Any]
    catalog: dict[str, Any]
    sections: tuple[HubSection, ...] = ()
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "theme": self.theme,
            "profile": self.profile,
            "daily_message": self.daily_message,
            "dashboard": self.dashboard,
            "guidance": self.guidance,
            "suggestions": self.suggestions,
            "calendar": self.calendar,
            "catalog": self.catalog,
            "sections": [section.to_dict() for section in self.sections],
        }
