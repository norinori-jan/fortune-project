from core.registry_a import load_registry
REGISTRY = load_registry()

STEMS = REGISTRY["shichu"]["stems"]
BRANCHES = REGISTRY["shichu"]["branches"]
TEN_GODS = REGISTRY["shichu"]["ten_gods"]
TWELVE_GROWTH = REGISTRY["shichu"]["twelve_growth"]
SIXTY_KANCHI = REGISTRY["shichu"]["sixty_kanchi"]
RELATIONS = REGISTRY["shichu"]["relations"]

# 蟷ｲ縺ｨ謾ｯ縺ｮ鬆・ｺ・
STEM_ORDER = [s["kanji"] for s in STEMS]
BRANCH_ORDER = [b["kanji"] for b in BRANCHES]

# 蜈ｭ蜊∝ｹｲ謾ｯ縺ｮ鬆・ｺ・
KANCHI_ORDER = [kc["name"] for kc in SIXTY_KANCHI]



def get_kanchi_index(stem: str, branch: str) -> int:
    """蟷ｲ謾ｯ縺ｮ繧､繝ｳ繝・ャ繧ｯ繧ｹ繧定ｿ斐☆・・縲・9・・""
    name = stem + branch
    return KANCHI_ORDER.index(name)


def get_year_pillar(year: int) -> str:
    """隘ｿ證ｦ縺九ｉ蟷ｴ譟ｱ・亥ｹｲ謾ｯ・峨ｒ霑斐☆"""
    # 1984蟷ｴ・育抜蟄撰ｼ峨ｒ蝓ｺ貅悶↓縺吶ｋ
    base_year = 1984
    offset = (year - base_year) % 60
    return KANCHI_ORDER[offset]


def get_month_pillar(year_stem: str, month: int) -> str:
    """
    譛域浤繧定ｿ斐☆・育ｰ｡譏鍋沿・・
    month: 1縲・2
    """
    # 蟷ｴ蟷ｲ縺九ｉ譛亥ｹｲ繧呈ｱｺ繧√ｋ・育ｰ｡譏灘ｼ擾ｼ・
    stem_index = STEM_ORDER.index(year_stem)
    month_stem = STEM_ORDER[(stem_index * 2 + month + 1) % 10]

    # 譛域髪縺ｯ蝗ｺ螳・
    month_branch = BRANCH_ORDER[(month + 1) % 12]

    return month_stem + month_branch


def get_day_pillar(day_index: int) -> str:
    """
    譌･譟ｱ・育ｰ｡譏鍋沿・・
    day_index: 0縲・9 縺ｮ譌･謨ｰ繧ｫ繧ｦ繝ｳ繧ｿ
    """
    return KANCHI_ORDER[day_index % 60]


def get_hour_pillar(day_stem: str, hour: int) -> str:
    """
    譎よ浤・育ｰ｡譏鍋沿・・
    hour: 0縲・3
    """
    # 譎よ髪
    branch_index = (hour + 1) // 2
    branch = BRANCH_ORDER[branch_index % 12]

    # 譌･蟷ｲ縺九ｉ譎ょｹｲ繧呈ｱｺ繧√ｋ
    stem_index = STEM_ORDER.index(day_stem)
    stem = STEM_ORDER[(stem_index * 2 + branch_index) % 10]

    return stem + branch
