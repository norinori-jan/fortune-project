from __future__ import annotations
from dataclasses import dataclass
from hashlib import sha256
from typing import Any
ELEMENTS = ("木", "火", "土", "金", "水")
@dataclass(frozen=True, slots=True)
class ElementBalance:
    values: dict[str, int]
    def dominant(self) -> str:
        return max(self.values, key=self.values.get)
    def lacking(self) -> str:
        return min(self.values, key=self.values.get)
    def to_dict(self) -> dict[str, Any]:
        return {
            "values": dict(self.values),
            "dominant": self.dominant(),
            "lacking": self.lacking(),
        }
class FiveElementService:
    def analyze(self, text: str) -> ElementBalance:
        text = text.strip()
        if not text:
            raise ValueError("text must not be empty")
        digest = sha256(text.encode("utf-8")).digest()
        values = {
            element: 1 + digest[index] % 10
            for index, element in enumerate(ELEMENTS)
        }
        return ElementBalance(values=values)
