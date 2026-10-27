from __future__ import annotations

import hashlib
from datetime import date

from fortune_core.models.runtime_daily import FortuneRuntimeDaily


class FortuneRuntimeDailyService:
    DIRECTIONS = (
        "東",
        "西",
        "南",
        "北",
        "北東",
        "南東",
        "南西",
        "北西",
    )

    MESSAGES = (
        "小さな変化を受け入れることで流れが整いやすい日です。",
        "焦らず一つずつ進めることが良い流れにつながります。",
        "身近な人との会話に新しい気づきがありそうです。",
        "今まで積み重ねてきたことを見直すのに向いた日です。",
        "新しい選択肢に目を向けることで可能性が広がります。",
    )

    ADVICE = (
        "最初に一番大切なことを一つ決めましょう。",
        "予定に少し余白を作りましょう。",
        "気になっていたことを一つ整理しましょう。",
        "誰かに感謝を伝える時間を作りましょう。",
        "直感で気になったことをメモしておきましょう。",
    )

    def get(
        self,
        *,
        user_key: str,
        theme: str = "general",
        target_date: date | None = None,
    ) -> FortuneRuntimeDaily:
        target = target_date or date.today()

        seed = hashlib.sha256(
            f"{user_key}:{theme}:{target.isoformat()}".encode()
        ).digest()

        index = int.from_bytes(seed[:4], "big")

        return FortuneRuntimeDaily(
            date=target.isoformat(),
            theme=theme,
            title=f"{target.isoformat()} の{theme}運",
            message=self.MESSAGES[
                index % len(self.MESSAGES)
            ],
            advice=self.ADVICE[
                index % len(self.ADVICE)
            ],
            lucky_keywords=(
                "整える",
                "対話",
                "一歩",
            ),
            lucky_number=(index % 9) + 1,
            lucky_direction=self.DIRECTIONS[
                index % len(self.DIRECTIONS)
            ],
        )