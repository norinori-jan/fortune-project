from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
@dataclass(frozen=True)
class FortuneCalendar:
    target_date: date
    week_start: date
    week_end: date
    month_start: date
    month_end: date
    year_start: date
    year_end: date
    def to_dict(self) -> dict[str, str]:
        return {
            "target_date": self.target_date.isoformat(),
            "week_start": self.week_start.isoformat(),
            "week_end": self.week_end.isoformat(),
            "month_start": self.month_start.isoformat(),
            "month_end": self.month_end.isoformat(),
            "year_start": self.year_start.isoformat(),
            "year_end": self.year_end.isoformat(),
        }
class FortuneCalendarService:
    def build(self, target_date: date | None = None) -> FortuneCalendar:
        target_date = target_date or date.today()
        monday_offset = target_date.weekday()
        week_start = target_date - timedelta(days=monday_offset)
        week_end = week_start + timedelta(days=6)
        month_start = target_date.replace(day=1)
        if target_date.month == 12:
            next_month = target_date.replace(
                year=target_date.year + 1,
                month=1,
                day=1,
            )
        else:
            next_month = target_date.replace(
                month=target_date.month + 1,
                day=1,
            )
        month_end = next_month - timedelta(days=1)
        year_start = target_date.replace(month=1, day=1)
        year_end = target_date.replace(month=12, day=31)
        return FortuneCalendar(
            target_date=target_date,
            week_start=week_start,
            week_end=week_end,
            month_start=month_start,
            month_end=month_end,
            year_start=year_start,
            year_end=year_end,
        )

fortune-core/fortune_core/services/calendar.py

from .fortune_calendar import FortuneCalendar, FortuneCalendarService
__all__ = [
    "FortuneCalendar",
    "FortuneCalendarService",
]