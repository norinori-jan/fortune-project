from dataclasses import dataclass, field

@dataclass
class Branch:
    name: str
    index: int
    hidden_stems: list = field(default_factory=list)