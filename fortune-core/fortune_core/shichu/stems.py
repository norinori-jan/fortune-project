from dataclasses import dataclass

@dataclass(frozen=True)
class Stem:
    name: str
    element: str
    yin_yang: str
    index: int
