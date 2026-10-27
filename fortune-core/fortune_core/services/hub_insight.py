from __future__ import annotations
import hashlib
from dataclasses import dataclass
from datetime import date
from ..models.hub_insight import (
    HubInsight,
    HubInsightCollection,
)
@dataclass(frozen=True)
class InsightTemplate:
    key: str
    title: str
    messages: tuple[str, ...]
    keywords: tuple[str, ...]
    actions: tuple[str, ...]
class FortuneHubInsightService:
    """
    Hub全体で表示する「今日の読み解き」を生成する。
    占術そのものではなく、日常行動に落とすための補助レイヤー。
    """
    TEMPLATES = {
        "general": (
            InsightTemplate(
                key="focus",
                title="今日の焦点",
                messages=(
                    "急いで答えを出すより、まず状況を整理する時間を持つ。",
                    "小さな変化を見逃さず、今日できることから始める。",
                    "一つのことに意識を向けると流れが整いやすい。",
                ),
                keywords=("整理", "観察", "一歩"),
                actions=(
                    "今日やることを一つ決める",
                    "不要な予定を一つ減らす",
                ),
            ),
            InsightTemplate(
                key="connection",
                title="人との流れ",
                messages=(
                    "短い言葉でも、丁寧に伝えることを意識する。",
                    "相手の話を最後まで聞くことで新しい視点が得られる。",
                    "一人で抱えず、必要なところでは人に相談する。",
                ),
                keywords=("対話", "理解", "協力"),
                actions=(
                    "一人に感謝を伝える",
                    "気になっていることを言葉にする",
                ),
            ),
        ),
        "love": (
            InsightTemplate(
                key="relationship",
                title="関係性の焦点",
                messages=(
                    "相手を変えるより、自分の伝え方を整える。",
                    "答えを急がず、相手のペースも尊重する。",
                    "小さな安心感を積み重ねることを意識する。",
                ),
                keywords=("信頼", "対話", "安心"),
                actions=(
                    "相手の話を遮らずに聞く",
                    "素直な感謝を一つ伝える",
                ),
            ),
        ),
        "work": (
            InsightTemplate(
                key="work",
                title="仕事の焦点",
                messages=(
                    "優先順位を一度整理すると、動きやすくなる。",
                    "大きな仕事を小さな単位に分けて進める。",
                    "周囲との認識を合わせてから作業を進める。",
                ),
                keywords=("優先順位", "集中", "共有"),
                actions=(
                    "最重要タスクを一つ決める",
                    "未整理のタスクを一覧化する",
                ),
            ),
        ),
        "money": (
            InsightTemplate(
                key="money",
                title="お金の焦点",
                messages=(
                    "大きな判断の前に、現在の支出を整理する。",
                    "必要なものと欲しいものを分けて考える。",
                    "短期的な気分より、継続できる習慣を重視する。",
                ),
                keywords=("整理", "計画", "継続"),
                actions=(
                    "今日の支出を確認する",
                    "今月の固定費を一度見直す",
                ),
            ),
        ),
        "health": (
            InsightTemplate(
                key="balance",
                title="生活の焦点",
                messages=(
                    "無理に変えようとせず、生活リズムを一つ整える。",
                    "休む時間も予定の一部として扱う。",
                    "小さな習慣を続けることを意識する。",
                ),
                keywords=("休息", "習慣", "バランス"),
                actions=(
                    "休憩時間を確保する",
                    "今日の生活リズムを一つ整える",
                ),
            ),
        ),
    }
    def generate(
        self,
        *,
        theme: str = "general",
        target_date: date | None = None,
        limit: int = 3,
    ) -> HubInsightCollection:
        current_date = target_date or date.today()
        templates = self.TEMPLATES.get(
            theme,
            self.TEMPLATES["general"],
        )
        seed = hashlib.sha256(
            f"{current_date.isoformat()}|{theme}".encode("utf-8")
        ).digest()
        insights: list[HubInsight] = []
        for index in range(min(limit, len(templates))):
            template = templates[
                (seed[index] + index) % len(templates)
            ]
            message_index = seed[index + 4] % len(template.messages)
            action_index = seed[index + 8] % len(template.actions)
            insights.append(
                HubInsight(
                    key=template.key,
                    title=template.title,
                    message=template.messages[message_index],
                    keywords=template.keywords,
                    actions=(template.actions[action_index],),
                    metadata={
                        "date": current_date.isoformat(),
                        "theme": theme,
                    },
                )
            )
        return HubInsightCollection(
            theme=theme,
            insights=tuple(insights),
        )