from dataclasses import dataclass
from .stems import Stem
from .branches import Branch


@dataclass(frozen=True)
class ZangKan:
    """蔵干（本気・中気・余気）"""
    main: Stem | None
    middle: Stem | None
    extra: Stem | None


class ZangKanEngine:
    """
    hidden_stems.json を使って
    Branch（十二支）→ ZangKan（蔵干）を返すエンジン
    """

    def __init__(self, registry_loader):
        self.stems = registry_loader.get_stems()
        self.hidden = registry_loader.get_hidden_stems()

    def get_zangkan(self, branch: Branch) -> ZangKan:
        data = self.hidden.get(branch.name)

        return ZangKan(
            main=self.stems.get(data["main"]) if data["main"] else None,
            middle=self.stems.get(data["middle"]) if data["middle"] else None,
            extra=self.stems.get(data["extra"]) if data["extra"] else None,
        )