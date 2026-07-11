from dataclasses import dataclass


@dataclass(frozen=True)
class Stem:
    """
    十干
    """

    name: str

    element: str

    yin_yang: str

    index: int