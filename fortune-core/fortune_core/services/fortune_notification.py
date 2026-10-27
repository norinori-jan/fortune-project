from __future__ import annotations
from datetime import date
import hashlib
from fortune_core.models.fortune_notification import (
    FortuneNotification,
)
class FortuneNotificationService:
    def build(
        self,
        question: str,
        target_date: date | None = None,
    ) -> tuple[FortuneNotification, ...]:
        target_date = target_date or date.today()
        seed = f"{question}|{target_date.isoformat()}"
        digest = hashlib.sha256(seed.encode("utf-8")).digest()
        return (
            FortuneNotification(
                notification_id="morning",
                title="朝の運勢",
                message="今日のテーマを一つ決めてスタートしましょう。",
                category="daily",
                timing="morning",
                enabled=True,
            ),
            FortuneNotification(
                notification_id="afternoon",
                title="昼の運勢",
                message=(
                    "午前中の流れを振り返り、"
                    "午後の優先順位を整えましょう。"
                ),
                category="daily",
                timing="afternoon",
                enabled=True,
            ),
            FortuneNotification(
                notification_id="evening",
                title="夜の運勢",
                message="今日できたことを確認して、明日の準備をしましょう。",
                category="daily",
                timing="evening",
                enabled=True,
            ),
            FortuneNotification(
                notification_id=f"daily-{digest[0]:02x}",
                title="今日のひとこと",
                message="小さな変化にも目を向けると、新しい発見につながります。",
                category="message",
                timing="daily",
                enabled=True,
            ),
        )
