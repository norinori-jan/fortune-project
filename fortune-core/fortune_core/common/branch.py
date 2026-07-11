from dataclasses import dataclass, field


@dataclass
class Branch:
    """
    十二支
    """

    name: str

    index: int

    hidden_stems: list = field(default_factory=list)

    season: str | None = None