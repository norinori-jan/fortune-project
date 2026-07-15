# fortune_core/shichu/relation.py

from dataclasses import dataclass
from itertools import combinations

from fortune_core.common.branch import Branch


@dataclass(frozen=True)
class RelationResult:
    kei: list[tuple[str, str]]
    chu: list[tuple[str, str]]
    gai: list[tuple[str, str]]
    gogo: list[tuple[str, str]]
    sango: list[str]
    hogo: list[str]
    kaikyoku: list[str]


class RelationEngine:
    """
    十二支の関係判定

    ・刑
    ・冲
    ・害
    ・六合
    ・三合
    ・方合
    ・会局
    """

    def __init__(self, registry_loader):

        self.master = registry_loader.get_relations()

# ------------------------------------------------------------
# 共通：三支グループ判定
# ------------------------------------------------------------
def _find_group(self, key: str, branches: list[Branch]) -> str | None:
    """
    三合・方合・会局の共通判定

    key:
        "三合"
        "方合"
        "会局"
    """

    names = {b.name for b in branches}
    checked = set()

    element_map = {
        ("申", "子", "辰"): "水",
        ("亥", "卯", "未"): "木",
        ("寅", "午", "戌"): "火",
        ("巳", "酉", "丑"): "金",

        ("亥", "子", "丑"): "水",
        ("寅", "卯", "辰"): "木",
        ("巳", "午", "未"): "火",
        ("申", "酉", "戌"): "金",
    }

    table = self.relations[key]

    for b in branches:

        if b.name in checked:
            continue

        combo = table.get(b.name)

        if combo is None:
            continue

        if set(combo).issubset(names):
            checked.update(combo)
            return element_map.get(tuple(combo))

    return None
    # ---------------------------------------------------------
    # 判定
    # ---------------------------------------------------------
    def determine(self, branches: list[Branch]) -> RelationResult:

        names = [b.name for b in branches]

        kei = []
        chu = []
        gai = []
        gogo = []
        sango = []
        hogo = []
        kaikyoku = []

        # -----------------------------
        # 刑・冲・害・六合
        # -----------------------------
        for a, b in combinations(names, 2):

            if b in self.master["刑"].get(a, []):
                kei.append((a, b))

            if self.master["冲"].get(a) == b:
                chu.append((a, b))

            if self.master["害"].get(a) == b:
                gai.append((a, b))

            if self.master["六合"].get(a) == b:
                gogo.append((a, b))

        # -----------------------------
        # 三合
        # -----------------------------
    def get_sango(self, branches: list[Branch]) -> str | None:
        names = {b.name for b in branches}

        checked = set()

        for b in branches:
            if b.name in checked:
                continue

            combo = self.relations["三合"].get(b.name)

            if combo and set(combo).issubset(names):

                if combo == ["申", "子", "辰"]:
                    return "水"

                if combo == ["亥", "卯", "未"]:
                    return "木"

                if combo == ["寅", "午", "戌"]:
                    return "火"

                if combo == ["巳", "酉", "丑"]:
                    return "金"

                checked.update(combo)

        return None
        checked = set()

        for name in names:

            group = tuple(sorted(self.master["三合"].get(name, [])))

            if not group:
                continue

            if group in checked:
                continue

            if set(group).issubset(names):
                sango.append("".join(group))
                checked.add(group)

        # -----------------------------
        # 方合
        # -----------------------------
    def get_hogo(self, branches: list[Branch]) -> str | None:
        names = {b.name for b in branches}

        checked = set()

        for b in branches:
            if b.name in checked:
                continue

            combo = self.relations["方合"].get(b.name)

            if combo and set(combo).issubset(names):

                if combo == ["亥", "子", "丑"]:
                    return "水"

                if combo == ["寅", "卯", "辰"]:
                    return "木"

                if combo == ["巳", "午", "未"]:
                    return "火"

                if combo == ["申", "酉", "戌"]:
                    return "金"

                checked.update(combo)

        return None    
        checked = set()

        for name in names:

            group = tuple(sorted(self.master["方合"].get(name, [])))

            if not group:
                continue

            if group in checked:
                continue

            if set(group).issubset(names):
                hogo.append("".join(group))
                checked.add(group)

        # -----------------------------
        # 会局
        # -----------------------------
    def get_kaikyoku(self, branches: list[Branch]) -> str | None:
        names = {b.name for b in branches}

        checked = set()

        for b in branches:
            if b.name in checked:
                continue

            combo = self.relations["会局"].get(b.name)

            if combo and set(combo).issubset(names):

                if combo == ["亥", "子", "丑"]:
                    return "水"

                if combo == ["寅", "卯", "辰"]:
                    return "木"

                if combo == ["巳", "午", "未"]:
                    return "火"

                if combo == ["申", "酉", "戌"]:
                    return "金"

                checked.update(combo)

        return None        
        checked = set()

        for name in names:

            group = tuple(sorted(self.master["会局"].get(name, [])))

            if not group:
                continue

            if group in checked:
                continue

            if set(group).issubset(names):
                kaikyoku.append("".join(group))
                checked.add(group)

        return RelationResult(
            kei=kei,
            chu=chu,
            gai=gai,
            gogo=gogo,
            sango=sango,
            hogo=hogo,
            kaikyoku=kaikyoku,
        )
    # ------------------------------------------------------------
    # 六合
    # ------------------------------------------------------------
    def is_rikugo(self, a: Branch, b: Branch) -> bool:
        return self.relations["六合"].get(a.name) == b.name

    # ------------------------------------------------------------
    # 冲
    # ------------------------------------------------------------
    def is_chong(self, a: Branch, b: Branch) -> bool:
        return self.relations["冲"].get(a.name) == b.name

    # ------------------------------------------------------------
    # 害
    # ------------------------------------------------------------
    def is_gai(self, a: Branch, b: Branch) -> bool:
        return self.relations["害"].get(a.name) == b.name

    # ------------------------------------------------------------
    # 刑
    # ------------------------------------------------------------
    def is_xing(self, a: Branch, b: Branch) -> bool:
        return b.name in self.relations["刑"].get(a.name, [])
    