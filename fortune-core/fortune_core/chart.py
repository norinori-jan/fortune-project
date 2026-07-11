from dataclasses import dataclass, field
from datetime import datetime

from .pillar import Pillar


@dataclass
class Chart:
    """
    命式全体
    """

    birth: datetime

    gender: str

    year: Pillar

    month: Pillar

    day: Pillar

    hour: Pillar

    five_elements: dict = field(default_factory=dict)

    useful_god: str | None = None

    favorable_gods: list = field(default_factory=list)

    unfavorable_gods: list = field(default_factory=list)

    strength: str | None = None

    empty_branches: list = field(default_factory=list)

    combinations: list = field(default_factory=list)

    clashes: list = field(default_factory=list)

    penalties: list = field(default_factory=list)

    harms: list = field(default_factory=list)

    luck_cycles: list = field(default_factory=list)

    annual_fortune: dict = field(default_factory=dict)

    monthly_fortune: dict = field(default_factory=dict)

    ai_notes: dict = field(default_factory=dict)