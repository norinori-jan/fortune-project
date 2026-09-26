from __future__ import annotations
from datetime import date
import hashlib
from fortune_core.models.dashboard import DashboardCard, FortuneDashboard
from fortune_core.services.fortune_themes import FortuneThemeService
from fortune_core.services.period_fortune import PeriodFortuneService
class FortuneDashboardService:
    def __init__(self) -> None:
        self.period_service = PeriodFortuneService()
        self.theme_service = FortuneThemeService()
    @staticmethod
    def _score(seed: str) -> int:
        digest = hashlib.sha256(seed.encode("utf-8")).digest()
        return 50 + digest[0] % 51
    @staticmethod
    def _keywords(period: str, score: int) -> tuple[str, ...]:
        if score >= 85:
            return ("好調", "前進", period)
        if score >= 70:
            return ("安定", "積み重ね", period)
        if score >= 60:
            return ("調整", "準備", period)
        return ("慎重", "見直し", period)
    def _period_card(
        self,
        question: str,
        period: str,
        target_date: date,
    ) -> DashboardCard:
        result = self.period_service.fortune(
            question=question,
            period=period,
            target_date=target_date,
        )
        return DashboardCard(
            key=period,
            title=result.title,
            score=result.score,
            message=result.message,
            advice=result.advice,
            keywords=self._keywords(period, result.score),
        )
    def build(
        self,
        question: str,
        target_date: date | None = None,
    ) -> FortuneDashboard:
        target_date = target_date or date.today()
        daily = self._period_card(question, "day", target_date)
        weekly = self._period_card(question, "month", target_date)
        yearly = self._period_card(question, "year", target_date)
        theme_cards: list[DashboardCard] = []
        for theme_key in ("love", "work", "money", "health", "general"):
            result = self.theme_service.fortune(
                question=question,
                theme=theme_key,
                target_date=target_date,
            )
            score = self._score(
                f"{question}|{theme_key}|{target_date.isoformat()}"
            )
            theme_cards.append(
                DashboardCard(
                    key=theme_key,
                    title=result.title,
                    score=score,
                    message=result.message,
                    advice=result.advice,
                    keywords=(
                        result.theme,
                        *result.keywords,
                    ),
                )
            )
        cards = [daily, weekly, yearly, *theme_cards]
        average = sum(card.score for card in cards) // len(cards)
        if average >= 85:
            overall_message = "全体的に流れが強く、行動を形にしやすい時期です。"
            overall_advice = "迷っていることは、小さな一歩から始めてみましょう。"
        elif average >= 70:
            overall_message = "安定した流れの中で、着実に積み上げられる時期です。"
            overall_advice = "優先順位を決めて、一つずつ進めると流れが整います。"
        elif average >= 60:
            overall_message = "大きく動くより、準備と調整を意識したい時期です。"
            overall_advice = "焦らず現状を整理してから次の行動を選びましょう。"
        else:
            overall_message = "今は流れを整えることを優先したい時期です。"
            overall_advice = "無理に結論を急がず、不要な負担を減らしましょう。"
        return FortuneDashboard(
            title="総合運ダッシュボード",
            date_key=target_date.isoformat(),
            daily=daily,
            weekly=weekly,
            yearly=yearly,
            themes=tuple(theme_cards),
            overall_message=overall_message,
            overall_advice=overall_advice,
        )