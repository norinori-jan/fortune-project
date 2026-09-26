from __future__ import annotations
from dataclasses import dataclass
from datetime import date, timedelta
import hashlib
@dataclass(frozen=True)
class TimelinePoint:
    date_key: str
    label: str
    score: int
    message: str
    def to_dict(self) -> dict[str, object]:
        return {
            "date": self.date_key,
            "label": self.label,
            "score": self.score,
            "message": self.message,
        }
class FortuneTimelineService:
    LABELS = (
        "始まり",
        "前進",
        "交流",
        "整理",
        "発見",
        "調整",
        "まとめ",
    )
    MESSAGES = (
        "新しい流れを作りやすい日です。",
        "小さな行動を積み重ねるのに向いています。",
        "人とのつながりを意識したい日です。",
        "不要なものを整理すると流れが整います。",
        "新しい視点を取り入れてみましょう。",
        "無理をせず、ペースを調整しましょう。",
        "一週間を振り返り、次につなげましょう。",
    )
    def build(
        self,
        question: str,
        start_date: date | None = None,
        days: int = 7,
    ) -> tuple[TimelinePoint, ...]:
        start_date = start_date or date.today()
        days = max(1, min(days, 31))
        points: list[TimelinePoint] = []
        for index in range(days):
            current = start_date + timedelta(days=index)
            seed = f"{question}|{current.isoformat()}"
            digest = hashlib.sha256(seed.encode("utf-8")).digest()
            score = 50 + digest[0] % 51
            label = self.LABELS[digest[1] % len(self.LABELS)]
            message = self.MESSAGES[digest[2] % len(self.MESSAGES)]
            points.append(
                TimelinePoint(
                    date_key=current.isoformat(),
                    label=label,
                    score=score,
                    message=message,
                )
            )
        return tuple(points)