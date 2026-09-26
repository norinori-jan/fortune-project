from __future__ import annotations
from datetime import date
import hashlib
from fortune_core.models.guidance import (
    FortuneAction,
    FortuneGuidance,
    LuckyGuide,
)
class FortuneGuidanceService:
    COLORS = (
        "白",
        "青",
        "緑",
        "金",
        "赤",
        "紫",
        "水色",
        "黄色",
    )
    DIRECTIONS = (
        "東",
        "西",
        "南",
        "北",
        "北東",
        "北西",
        "南東",
        "南西",
    )
    ITEMS = (
        "ノート",
        "時計",
        "ペン",
        "本",
        "小さな植物",
        "お気に入りの飲み物",
        "音楽",
        "写真",
    )
    def _digest(self, seed: str) -> bytes:
        return hashlib.sha256(seed.encode("utf-8")).digest()
    def build(
        self,
        question: str,
        target_date: date | None = None,
    ) -> FortuneGuidance:
        target_date = target_date or date.today()
        seed = f"{question}|{target_date.isoformat()}"
        digest = self._digest(seed)
        actions = (
            FortuneAction(
                category="start",
                title="最初の一歩を決める",
                description="今日やることを一つだけ具体化しましょう。",
                priority="high",
                timing="午前",
            ),
            FortuneAction(
                category="connection",
                title="人とのつながりを整える",
                description="短い連絡や感謝の言葉を一つ届けましょう。",
                priority="medium",
                timing="昼",
            ),
            FortuneAction(
                category="review",
                title="一日の振り返り",
                description="できたことを確認して、次の一手を決めましょう。",
                priority="medium",
                timing="夜",
            ),
        )
        lucky = LuckyGuide(
            color=self.COLORS[digest[0] % len(self.COLORS)],
            number=(digest[1] % 9) + 1,
            direction=self.DIRECTIONS[digest[2] % len(self.DIRECTIONS)],
            item=self.ITEMS[digest[3] % len(self.ITEMS)],
            keyword=("前進", "調和", "整理", "発見")[digest[4] % 4],
        )
        timeline = (
            "朝：優先順位を一つ決める",
            "昼：人との交流または情報収集",
            "夕：成果を確認する",
            "夜：明日の準備をする",
        )
        caution = (
            "情報を一度に詰め込みすぎず、重要なことから順番に進めましょう。"
        )
        return FortuneGuidance(
            actions=actions,
            lucky=lucky,
            timeline=timeline,
            caution=caution,
        )