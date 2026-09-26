from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Any
@dataclass(frozen=True)
class FortuneAction:
    category: str
    title: str
    description: str
    priority: str
    timing: str
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
@dataclass(frozen=True)
class LuckyGuide:
    color: str
    number: int
    direction: str
    item: str
    keyword: str
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
@dataclass(frozen=True)
class FortuneGuidance:
    actions: tuple[FortuneAction, ...]
    lucky: LuckyGuide
    timeline: tuple[str, ...]
    caution: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "actions": [item.to_dict() for item in self.actions],
            "lucky": self.lucky.to_dict(),
            "timeline": list(self.timeline),
            "caution": self.caution,
        }