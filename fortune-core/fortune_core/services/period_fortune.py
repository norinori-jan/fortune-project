from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
@dataclass(frozen=True, slots=True)
class PeriodFortune:
    period: str
    score: int
    title: str
    message: str
    advice: str
    def to_dict(self) -> dict:
        return {
            "period": self.period,
            "score": self.score,
            "title": self.title,
            "message": self.message,
            "advice": self.advice,
        }
class PeriodFortuneService:
    TITLES = (
        "始動",
        "安定",
        "成長",
        "転換",
        "発見",
        "調整",
    )
    MESSAGES = (
        "新しいことを始めるきっかけを作りやすい時です。",
        "基礎を整えることで安定した流れを作れます。",
        "継続してきたことに変化が現れやすい時です。",
        "これまでの方法を見直すことで新しい方向が見えてきます。",
        "普段と違う情報や人からヒントを得られそうです。",
        "急がず全体のバランスを整えることが重要です。",
    )
    def divine(
        self,
        target_date: date,
        period: str = "day",
    ) -> PeriodFortune:
        if period not in {"day", "month", "year"}:
            raise ValueError(
                "period must be day, month, or year"
            )
        seed = self._seed(target_date, period)
        score = 50 + seed % 51
        index = seed % len(self.TITLES)
        advice = (
            "小さな行動を一つ決めてください。"
            if score < 75
            else "流れを活かして、できることを一つ前に進めてください。"
        )
        return PeriodFortune(
            period=period,
            score=score,
            title=self.TITLES[index],
            message=self.MESSAGES[index],
            advice=advice,
        )
    @staticmethod
    def _seed(target_date: date, period: str) -> int:
        if period == "day":
            value = target_date.isoformat()
        elif period == "month":
            value = f"{target_date.year:04d}-{target_date.month:02d}"
        else:
            value = str(target_date.year)
        digest = sha256(
            f"{period}:{value}".encode("utf-8")
        ).digest()
        return int.from_bytes(digest[:8], "big")