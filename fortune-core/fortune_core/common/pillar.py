from dataclasses import dataclass, field

from .stem import Stem
from .branch import Branch


@dataclass
class Pillar:
    """
    年柱・月柱・日柱・時柱
    """

    stem: Stem

    branch: Branch

    hidden_stems: list = field(default_factory=list)

    ten_god: str | None = None

    twelve_stage: str | None = None

    strength: str | None = None

    memo: str = ""
