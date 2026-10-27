from __future__ import annotations
from dataclasses import dataclass
from typing import Any
@dataclass(frozen=True)
class FortuneCompareItem:
    system: str
    title: str
    message: str
    advice: str
    def to_dict(self) -> dict[str, Any]:
        return {
            "system": self.system,
            "title": self.title,
            "message": self.message,
            "advice": self.advice,
        }
@dataclass(frozen=True)
class FortuneComparison:
    question: str
    items: tuple[FortuneCompareItem, ...]
    def to_dict(self) -> dict[str, Any]:
        return {
            "question": self.question,
            "items": [
                item.to_dict()
                for item in self.items
            ],
        }

# [貼り付けメモ] 以降は別ファイルとして復元済み（元の文字は git 履歴に残っています）
