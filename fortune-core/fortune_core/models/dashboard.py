from __future__ import annotations
from dataclasses import asdict, dataclass
from typing import Any
@dataclass(frozen=True)
class DashboardCard:
    key: str
    title: str
    score: int
    message: str
    advice: str
    keywords: tuple[str, ...]
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
@dataclass(frozen=True)
class FortuneDashboard:
    title: str
    date_key: str
    daily: DashboardCard
    weekly: DashboardCard
    yearly: DashboardCard
    themes: tuple[DashboardCard, ...]
    overall_message: str
    overall_advice: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "date_key": self.date_key,
            "daily": self.daily.to_dict(),
            "weekly": self.weekly.to_dict(),
            "yearly": self.yearly.to_dict(),
            "themes": [item.to_dict() for item in self.themes],
            "overall_message": self.overall_message,
            "overall_advice": self.overall_advice,
        }