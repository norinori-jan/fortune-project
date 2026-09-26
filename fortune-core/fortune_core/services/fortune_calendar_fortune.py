from __future__ import annotations
from datetime import date, timedelta
import hashlib
from fortune_core.models.fortune_calendar_entry import (
    FortuneCalendarEntry,
)
class FortuneCalendarFortuneService:
    KEYWORDS = (
        "前進",
        "整理",
        "交流",
        "発見",
        "成長",
        "安定",
        "変化",
        "準備",
    )
    def build(
        self,
        question: str,
        start_date: date | None = None,
        days: int = 30,
    ) -> tuple[FortuneCalendarEntry, ...]:
        start_date = start_date or date.today()
        days = max(1, min(days, 366))
        result: list[FortuneCalendarEntry] = []
        for offset in range(days):
            current = start_date + timedelta(days=offset)
            digest = hashlib.sha256(
                f"{question}|{current.isoformat()}".encode("utf-8")
            ).digest()
            score = 50 + digest[0] % 51
            keyword = self.KEYWORDS[
                digest[1] % len(self.KEYWORDS)
            ]
            if score >= 85:
                title = "流れを活かす日"
                message = "行動を具体化すると進展につながりやすい日です。"
            elif score >= 70:
                title = "安定して進める日"
                message = "いつものペースを大切にするとよい日です。"
            elif score >= 60:
                title = "整える日"
                message = "準備や見直しを意識したい日です。"
            else:
                title = "ゆっくり進む日"
                message = "無理に急がず、余裕を残して過ごしましょう。"
            result.append(
                FortuneCalendarEntry(
                    date_key=current.isoformat(),
                    score=score,
                    title=title,
                    message=message,
                    keyword=keyword,
                )
            )
        return tuple(result)
