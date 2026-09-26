from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable
@dataclass(frozen=True)
class FortuneSummary:
    headline: str
    message: str
    advice: str
    tags: tuple[str, ...]
    def to_dict(self) -> dict[str, object]:
        return {
            "headline": self.headline,
            "message": self.message,
            "advice": self.advice,
            "tags": list(self.tags),
        }
class FortuneSummaryService:
    def build(
        self,
        scores: Iterable[int],
    ) -> FortuneSummary:
        values = list(scores)
        if not values:
            return FortuneSummary(
                headline="運勢を整える一日",
                message="まずは現在の状況を整理しましょう。",
                advice="小さな行動から始めることを意識してください。",
                tags=("整理", "準備"),
            )
        average = sum(values) // len(values)
        if average >= 85:
            return FortuneSummary(
                headline="流れを活かすタイミング",
                message="複数の運勢が前向きな流れを示しています。",
                advice="思いついたことを具体的な行動へ変えていきましょう。",
                tags=("前進", "行動", "好機"),
            )
        if average >= 70:
            return FortuneSummary(
                headline="安定を積み重ねるタイミング",
                message="大きく崩れにくい流れの中で着実に進めます。",
                advice="優先順位を決め、一つずつ完成させましょう。",
                tags=("安定", "継続", "成長"),
            )
        if average >= 60:
            return FortuneSummary(
                headline="整えながら進むタイミング",
                message="準備と調整を意識すると流れを作りやすくなります。",
                advice="急がず、必要なものから順番に整えましょう。",
                tags=("調整", "準備", "整理"),
            )
        return FortuneSummary(
            headline="立て直しを意識するタイミング",
            message="今は無理に広げず、足元を整えることを意識しましょう。",
            advice="負担になっていることを一つ減らしてみましょう。",
            tags=("休息", "整理", "再出発"),
        )