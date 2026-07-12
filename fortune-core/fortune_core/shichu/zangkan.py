# fortune_core/shichu/zangkan.py
from dataclasses import dataclass
from fortune_core.common.stem import Stem
from fortune_core.common.branch import Branch


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
        self.stems = registry_loader.get_stems()            # Stem オブジェクト
        self.hidden = registry_loader.get_hidden_stems()    # hidden_stems.json

    def get_zangkan(self, branch: Branch) -> ZangKan:
        """
        十二支 → 蔵干（本気・中気・余気）を返す
        """
        data = self.hidden.get(branch.name)

        return ZangKan(
            main=self.stems.get(data["main"]) if data["main"] else None,
            middle=self.stems.get(data["middle"]) if data["middle"] else None,
            extra=self.stems.get(data["extra"]) if data["extra"] else None
        )

