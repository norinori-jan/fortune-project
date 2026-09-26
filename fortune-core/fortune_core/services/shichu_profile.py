from __future__ import annotations
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from typing import Any
STEMS = (
    "甲", "乙", "丙", "丁", "戊",
    "己", "庚", "辛", "壬", "癸",
)
BRANCHES = (
    "子", "丑", "寅", "卯", "辰", "巳",
    "午", "未", "申", "酉", "戌", "亥",
)
@dataclass(frozen=True, slots=True)
class ShichuProfile:
    birth_date: str
    day_stem: str
    day_branch: str
    element: str
    keywords: tuple[str, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "birth_date": self.birth_date,
            "day_stem": self.day_stem,
            "day_branch": self.day_branch,
            "element": self.element,
            "keywords": list(self.keywords),
        }
class ShichuProfileService:
    def create(self, birth_date: date) -> ShichuProfile:
        raw = birth_date.isoformat()
        digest = sha256(raw.encode("utf-8")).digest()
        stem = STEMS[digest[0] % len(STEMS)]
        branch = BRANCHES[digest[1] % len(BRANCHES)]
        elements = ("木", "火", "土", "金", "水")
        element = elements[digest[2] % len(elements)]
        keywords = (
            f"{element}の性質",
            "日柱",
            "五行",
        )
        return ShichuProfile(
            birth_date=raw,
            day_stem=stem,
            day_branch=branch,
            element=element,
            keywords=keywords,
        )