from __future__ import annotations

from fortune_core.models.hub_widget import FortuneHubWidget


class FortuneHubWidgetService:
    def build_navigation(
        self,
        theme: str,
    ) -> list[FortuneHubWidget]:
        return [
            FortuneHubWidget(
                key="today",
                title="今日の運勢",
                widget_type="fortune-card",
                priority=1,
                actions=("open_today",),
            ),
            FortuneHubWidget(
                key="question",
                title="質問して占う",
                widget_type="question-input",
                priority=2,
                data={"theme": theme},
                actions=("ask",),
            ),
            FortuneHubWidget(
                key="tarot",
                title="タロット",
                widget_type="system-card",
                priority=3,
                data={"system": "tarot"},
                actions=("draw_tarot",),
            ),
            FortuneHubWidget(
                key="meihua",
                title="梅花易数",
                widget_type="system-card",
                priority=4,
                data={"system": "meihua"},
                actions=("draw_meihua",),
            ),
            FortuneHubWidget(
                key="elements",
                title="五行",
                widget_type="system-card",
                priority=5,
                data={"system": "five-elements"},
                actions=("analyze_elements",),
            ),
        ]