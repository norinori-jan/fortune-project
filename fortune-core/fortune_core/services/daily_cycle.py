from __future__ import annotations
from datetime import date
import hashlib
from fortune_core.models.daily_cycle import (
    DailyCycle,
    DailyCycleItem,
)
class DailyCycleService:
    PERIODS = (
        (
            "morning",
            "朝",
            "新しいことを始める時間",
            "今日の方向性を決めましょう。",
        ),
        (
            "afternoon",
            "昼",
            "行動を進める時間",
            "優先順位を一つに絞って進めましょう。",
        ),
        (
            "evening",
            "夜",
            "整理と振り返りの時間",
            "今日の成果を確認しましょう。",
        ),
    )
    def build(
        self,
        question: str,
        target_date: date | None = None,
    ) -> DailyCycle:
        target_date = target_date or date.today()
        items: list[DailyCycleItem] = []
        for index, (
            period,
            label,
            title,
            advice,
        ) in enumerate(self.PERIODS):
            seed = (
                f"{question}|"
                f"{target_date.isoformat()}|"
                f"{period}"
            )
            digest = hashlib.sha256(
                seed.encode("utf-8")
            ).digest()
            score = 50 + digest[index] % 51
            if score >= 85:
                message = "流れを活かして積極的に動きやすい時間です。"
            elif score >= 70:
                message = "安定したペースで進めやすい時間です。"
            elif score >= 60:
                message = "状況を確認しながら進めたい時間です。"
            else:
                message = "無理をせず、整理を優先したい時間です。"
            items.append(
                DailyCycleItem(
                    period=period,
                    title=f"{label}：{title}",
                    score=score,
                    message=message,
                    advice=advice,
                )
            )
        return DailyCycle(
            date_key=target_date.isoformat(),
            items=tuple(items),
        )