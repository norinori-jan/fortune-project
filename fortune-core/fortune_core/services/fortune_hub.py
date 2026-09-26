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
        birth_date: str | None = None,
        question: str = "",
        theme: str = "general",
        today: date | None = None,
    ) -> FortuneHubHome:
        target_date = today or date.today()
        profile = self.profile_service.create(
            birth_date=birth_date,
        )
        daily_message = self.message_service.generate(
            question=question,
            theme=theme,
            target_date=target_date,
        )
        dashboard = self.dashboard_service.build(
            question=question,
            theme=theme,
            today=target_date,
        )
        guidance = self.guidance_service.generate(
            question=question,
            theme=theme,
            target_date=target_date,
        )
        suggestions = self.suggestion_service.suggest(
            theme=theme,
            limit=6,
        )
        calendar = self.calendar_service.get(
            target_date=target_date,
            theme=theme,
        )
        catalog = self.catalog_service.catalog()
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
                summary=guidance.summary,
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
                summary=calendar.summary,
                data=calendar.to_dict(),
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
    def quick(
        self,
        *,
        question: str = "",
        theme: str = "general",
        today: date | None = None,
    ) -> dict[str, Any]:
        target_date = today or date.today()
        message = self.message_service.generate(
            question=question,
            theme=theme,
            target_date=target_date,
        )
        guidance = self.guidance_service.generate(
            question=question,
            theme=theme,
            target_date=target_date,
        )
        return {
            "question": question,
            "theme": theme,
            "date": target_date.isoformat(),
            "message": self._to_dict(message),
            "guidance": self._to_dict(guidance),
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