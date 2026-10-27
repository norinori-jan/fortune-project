from __future__ import annotations
from dataclasses import dataclass
import hashlib
from typing import Any
TRIGRAMS = (
    ("乾", "天"),
    ("兌", "沢"),
    ("離", "火"),
    ("震", "雷"),
    ("巽", "風"),
    ("坎", "水"),
    ("艮", "山"),
    ("坤", "地"),
)
@dataclass(frozen=True, slots=True)
class MeihuaResult:
    question: str
    upper: str
    lower: str
    moving_line: int
    message: str
    advice: str

    @property
    def title(self) -> str:
        return f"{self.upper}{self.lower}"

    @property
    def trigram_name(self) -> str:
        return f"上卦{self.upper}・下卦{self.lower}"

    @property
    def keywords(self) -> tuple[str, ...]:
        return (self.upper, self.lower, f"第{self.moving_line}爻")

    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "upper": self.upper,
            "lower": self.lower,
            "moving_line": self.moving_line,
            "message": self.message,
            "advice": self.advice,
        }
class MeihuaFortuneService:
    def divine(self, question: str) -> MeihuaResult:
        question = question.strip()
        if not question:
            raise ValueError("question must not be empty")
        digest = hashlib.sha256(question.encode("utf-8")).digest()
        upper = TRIGRAMS[digest[0] % 8][0]
        lower = TRIGRAMS[digest[1] % 8][0]
        moving_line = digest[2] % 6 + 1
        upper_element = TRIGRAMS[digest[0] % 8][1]
        lower_element = TRIGRAMS[digest[1] % 8][1]
        return MeihuaResult(
            question=question,
            upper=upper,
            lower=lower,
            moving_line=moving_line,
            message=(
                f"上卦は{upper}、下卦は{lower}。"
                f"{upper_element}と{lower_element}の組み合わせから、"
                "状況の変化を観察することが重要です。"
            ),
            advice=(
                f"第{moving_line}爻を変化点として考え、"
                "急いで結論を出さず流れを確認してください。"
            ),
        )
