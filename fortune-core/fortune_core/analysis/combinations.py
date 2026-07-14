# fortune_core/analysis/combinations.py

from dataclasses import dataclass
from fortune_core.common.branch import Branch
from fortune_core.shichu.relation import RelationEngine


@dataclass(frozen=True)
class CombinationResult:
    """
    地支の関係判定結果
    """
    rikugo: list[tuple[str, str]]
    sango: str | None
    hogo: str | None
    kei: list[tuple[str, str]]
    chong: list[tuple[str, str]]
    gai: list[tuple[str, str]]


class CombinationAnalyzer:
    """
    地支同士の関係を総合判定する
    """

    def __init__(self, registry_loader):
        self.relation = RelationEngine(registry_loader)

    def analyze(self, branches: list[Branch]) -> CombinationResult:

        rikugo = []
        kei = []
        chong = []
        gai = []

        # -----------------------------
        # 二支関係
        # -----------------------------
        for i in range(len(branches)):
            for j in range(i + 1, len(branches)):

                a = branches[i]
                b = branches[j]

                if self.relation.is_rikugo(a, b):
                    rikugo.append((a.name, b.name))

                if self.relation.is_kei(a, b):
                    kei.append((a.name, b.name))

                if self.relation.is_chong(a, b):
                    chong.append((a.name, b.name))

                if self.relation.is_gai(a, b):
                    gai.append((a.name, b.name))

        # -----------------------------
        # 三合・方合
        # -----------------------------
        sango = self.relation.find_sango(branches)
        hogo = self.relation.find_hogo(branches)

        return CombinationResult(
            rikugo=rikugo,
            sango=sango,
            hogo=hogo,
            kei=kei,
            chong=chong,
            gai=gai,
        )