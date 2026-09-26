from __future__ import annotations
import hashlib
from datetime import date
from ..models.hub_action import HubAction
class FortuneHubActionService:
    ACTIONS = {
        "general": (
            (
                "整理",
                "情報を整理する",
                "今抱えていることを紙やメモに書き出す。",
            ),
            (
                "focus",
                "一つに集中する",
                "今日最も重要なことを一つ決めて取り組む。",
            ),
            (
                "rest",
                "余白を作る",
                "予定の間に短い休憩時間を入れる。",
            ),
        ),
        "love": (
            (
                "listen",
                "話を聞く",
                "相手の話を最後まで聞く時間を作る。",
            ),
            (
                "thanks",
                "感謝を伝える",
                "身近な人に短い感謝の言葉を伝える。",
            ),
            (
                "space",
                "適度な距離を保つ",
                "相手にも自分にも考える時間を残す。",
            ),
        ),
        "work": (
            (
                "priority",
                "優先順位を決める",
                "最重要タスクを一つ決めてから動く。",
            ),
            (
                "share",
                "認識を合わせる",
                "必要な相手と目的や期限を確認する。",
            ),
            (
                "finish",
                "小さく完了させる",
                "大きな仕事を一つの完了単位に分ける。",
            ),
        ),
        "money": (
            (
                "check",
                "支出を確認する",
                "今日の支出を一度整理する。",
            ),
            (
                "plan",
                "予定を立てる",
                "今月の大きな支出を確認する。",
            ),
            (
                "avoid",
                "衝動を一度止める",
                "購入前に本当に必要か確認する。",
            ),
        ),
        "health": (
            (
                "rest",
                "休息を確保する",
                "短い休憩を意識的に取る。",
            ),
            (
                "routine",
                "生活リズムを整える",
                "今日の睡眠・食事・活動の一つを整える。",
            ),
            (
                "walk",
                "軽く体を動かす",
                "無理のない範囲で少し歩く。",
            ),
        ),
    }
    def generate(
        self,
        *,
        theme: str = "general",
        target_date: date | None = None,
        limit: int = 3,
    ) -> list[HubAction]:
        current_date = target_date or date.today()
        actions = self.ACTIONS.get(
            theme,
            self.ACTIONS["general"],
        )
        seed = hashlib.sha256(
            f"{theme}|{current_date.isoformat()}".encode("utf-8")
        ).digest()
        rotated = sorted(
            enumerate(actions),
            key=lambda pair: (
                seed[pair[0] % len(seed)],
                pair[0],
            ),
        )
        result: list[HubAction] = []
        for priority, (_, action) in enumerate(
            rotated[:limit],
            start=1,
        ):
            key, title, description = action
            result.append(
                HubAction(
                    key=key,
                    title=title,
                    description=description,
                    category=theme,
                    priority=priority,
                    metadata={
                        "date": current_date.isoformat(),
                    },
                )
            )
        return result