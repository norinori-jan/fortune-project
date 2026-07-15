from dataclasses import dataclass, field


@dataclass(frozen=True)
class Branch:
    name: str
    index: int
    yin_yang: str
    element: str | None = None
    hidden_stems: list = field(default_factory=list)