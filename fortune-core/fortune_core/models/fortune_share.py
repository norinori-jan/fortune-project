from __future__ import annotations
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class FortuneShare:
    """共有用の最小データ（取り込み時に欠けていたため、FortuneShareService の使い方から再作成）。"""
    share_id: str
    title: str
    message: str
    advice: str
    system: str
    theme: str
    date_key: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "share_id": self.share_id,
            "title": self.title,
            "message": self.message,
            "advice": self.advice,
            "system": self.system,
            "theme": self.theme,
            "date": self.date_key,
        }
