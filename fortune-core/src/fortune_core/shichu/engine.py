from core.registry_a import load_registry
REGISTRY = load_registry()

STEMS = REGISTRY["shichu"]["stems"]
BRANCHES = REGISTRY["shichu"]["branches"]
TEN_GODS = REGISTRY["shichu"]["ten_gods"]
TWELVE_GROWTH = REGISTRY["shichu"]["twelve_growth"]
SIXTY_KANCHI = REGISTRY["shichu"]["sixty_kanchi"]
RELATIONS = REGISTRY["shichu"]["relations"]

# 干と支の順序
STEM_ORDER = [s["kanji"] for s in STEMS]
BRANCH_ORDER = [b["kanji"] for b in BRANCHES]

# 六十干支の順序
KANCHI_ORDER = [kc["name"] for kc in SIXTY_KANCHI]



def get_kanchi_index(stem: str, branch: str) -> int:
    """干支のインデックスを返す（0〜59）"""
    name = stem + branch
    return KANCHI_ORDER.index(name)


def get_year_pillar(year: int) -> str:
    """西暦から年柱（干支）を返す"""
    # 1984年（甲子）を基準にする
    base_year = 1984
    offset = (year - base_year) % 60
    return KANCHI_ORDER[offset]


def get_month_pillar(year_stem: str, month: int) -> str:
    """
    月柱を返す（簡易版）
    month: 1〜12
    """
    # 年干から月干を決める（簡易式）
    stem_index = STEM_ORDER.index(year_stem)
    month_stem = STEM_ORDER[(stem_index * 2 + month + 1) % 10]

    # 月支は固定
    month_branch = BRANCH_ORDER[(month + 1) % 12]

    return month_stem + month_branch


def get_day_pillar(day_index: int) -> str:
    """
    日柱（簡易版）
    day_index: 0〜59 の日数カウンタ
    """
    return KANCHI_ORDER[day_index % 60]


def get_hour_pillar(day_stem: str, hour: int) -> str:
    """
    時柱（簡易版）
    hour: 0〜23
    """
    # 時支
    branch_index = (hour + 1) // 2
    branch = BRANCH_ORDER[branch_index % 12]

    # 日干から時干を決める
    stem_index = STEM_ORDER.index(day_stem)
    stem = STEM_ORDER[(stem_index * 2 + branch_index) % 10]

    return stem + branch
