from __future__ import annotations
from datetime import date, datetime
from typing import Any
from ..models.hub_home import FortuneHubHome, HubSection
from .fortune_calendar_fortune import FortuneCalendarFortuneService
from .fortune_catalog import FortuneCatalogService
from .fortune_profile import FortuneProfileService
from .fortune_message import FortuneMessageService
from .dashboard_fortune import FortuneDashboardService
from .guidance_fortune import FortuneGuidanceService
from .question_suggestions import QuestionSuggestionService
class FortuneHubService:
    """
    Fortune Hub の最上位オーケストレーター。
    個別の占術ロジックは各サービスに委譲し、
    Hub では「ホーム画面に必要な情報を束ねる」ことだけを担当する。
    """
    def __init__(self) -> None:
        self.profile_service = FortuneProfileService()
        self.message_service = FortuneMessageService()
        self.dashboard_service = FortuneDashboardService()
        self.guidance_service = FortuneGuidanceService()
        self.suggestion_service = QuestionSuggestionService()
        self.calendar_service = FortuneCalendarFortuneService()
        self.catalog_service = FortuneCatalogService()
    def home(
        self,
        *,
        user_key: str | None = None,
        birth_date: str | None = None,
        question: str = "",
        theme: str = "general",
        today: date | None = None,
    ) -> FortuneHubHome:
        target_date = today or date.today()
        profile = self.profile_service.create(
            birth_date=birth_date,
        )
        daily_message = self.message_service.build(
            question=question,
            target_date=target_date,
        )
        dashboard = self.dashboard_service.build(
            question=question,
            target_date=target_date,
        )
        guidance = self.guidance_service.build(
            question=question,
            target_date=target_date,
        )
        suggestions = self.suggestion_service.suggest(
            theme=theme,
        )[:6]
        calendar = self._calendar(question, target_date)
        catalog = self._catalog()
        sections = (
            HubSection(
                key="daily",
                title="今日の運勢",
                summary=daily_message.message,
                data=daily_message.to_dict(),
            ),
            HubSection(
                key="guidance",
                title="今日のガイド",
                summary=(guidance.actions[0].description if guidance.actions else guidance.caution),
                data=guidance.to_dict(),
            ),
            HubSection(
                key="suggestions",
                title="おすすめの占い",
                summary="今のテーマに合わせた質問と占術を提案します。",
                data={
                    "items": [
                        item.to_dict()
                        for item in suggestions
                    ]
                },
            ),
            HubSection(
                key="calendar",
                title="運勢カレンダー",
                summary=calendar["summary"],
                data=calendar,
            ),
        )
        return FortuneHubHome(
            question=question,
            theme=theme,
            profile=self._to_dict(profile),
            daily_message=self._to_dict(daily_message),
            dashboard=self._to_dict(dashboard),
            guidance=self._to_dict(guidance),
            suggestions=[
                self._to_dict(item)
                for item in suggestions
            ],
            calendar=self._to_dict(calendar),
            catalog=self._to_dict(catalog),
            sections=sections,
        )
    def today(
        self,
        *,
        user_key: str | None = None,
        theme: str = "general",
    ) -> Any:
        from .today_view import FortuneTodayViewService
        return FortuneTodayViewService().build(
            user_key=user_key or "guest",
            theme=theme,
        )

    def quick(
        self,
        *,
        user_key: str | None = None,
        question: str = "",
        theme: str = "general",
        today: date | None = None,
    ) -> dict[str, Any]:
        target_date = today or date.today()
        message = self.message_service.build(
            question=question,
            target_date=target_date,
        )
        guidance = self.guidance_service.build(
            question=question,
            target_date=target_date,
        )
        return {
            "question": question,
            "theme": theme,
            "date": target_date.isoformat(),
            "message": self._to_dict(message),
            "guidance": self._to_dict(guidance),
        }
    def _calendar(self, question: str, target_date: date) -> dict[str, Any]:
        """今日から30日の運勢カレンダー（各サービスは、日ごとの一覧を返す）。"""
        entries = self.calendar_service.build(question, start_date=target_date, days=30)
        items = [self._to_dict(e) for e in entries]
        return {"summary": "今日から30日間の運勢カレンダーです。", "days": len(items), "entries": items}

    def _catalog(self) -> dict[str, Any]:
        return {
            "systems": [self._to_dict(i) for i in self.catalog_service.systems()],
            "themes": [self._to_dict(i) for i in self.catalog_service.themes()],
        }

    @staticmethod
    def _to_dict(value: Any) -> dict[str, Any]:
        if hasattr(value, "to_dict"):
            return value.to_dict()
        if hasattr(value, "__dict__"):
            return dict(value.__dict__)
        if isinstance(value, dict):
            return value
        return {"value": value}