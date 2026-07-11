from __future__ import annotations

import random
from datetime import datetime, timezone
from functools import lru_cache
from .registry_loader import load_registry

# ---------------------------------------------------------------------------
# 繝昴ず繧ｷ繝ｧ繝ｳ螳夂ｾｩ・域諺蜈･鬆・ｺ上′螻暮幕鬆・ｼ・
# ---------------------------------------------------------------------------
CELTIC_CROSS_POSITIONS: list[tuple[str, str]] = [
    ("CURRENT_SITUATION",   "迴ｾ蝨ｨ縺ｮ迥ｶ豕・),
    ("CROSSING_CHALLENGE",  "隱ｲ鬘後・莠､蟾ｮ縺吶ｋ繧ゅ・"),
    ("DISTANT_PAST",        "驕縺・℃蜴ｻ繝ｻ譬ｹ蠎輔↓縺ゅｋ繧ゅ・"),
    ("RECENT_PAST",         "霑代＞驕主悉縺ｮ蠖ｱ髻ｿ"),
    ("BEST_OUTCOME",        "諢剰ｭ倥・譛蝟・・邨先棡"),
    ("IMMEDIATE_FUTURE",    "霑第悴譚･縺ｮ譁ｹ蜷第ｧ"),
    ("SELF_PERCEPTION",     "閾ｪ蟾ｱ隱崎ｭ倥・蜀・擇"),
    ("EXTERNAL_INFLUENCES", "螟夜Κ迺ｰ蠅・・莉冶・・蠖ｱ髻ｿ"),
    ("HOPES_AND_FEARS",     "蟶梧悍縺ｨ諱舌ｌ"),
    ("FINAL_OUTCOME",       "譛邨ら噪縺ｪ邨先忰"),
]

# ---------------------------------------------------------------------------
# TarotEngine・・SOT迚茨ｼ・
# ---------------------------------------------------------------------------

class TarotEngine:
    """
    繧ｿ繝ｭ繝・ヨ繧ｨ繝ｳ繧ｸ繝ｳ・・SOT: core/registry_a.json 繧貞盾辣ｧ・・

    78 譫壹・繝輔Ν繝・ャ繧ｭ繧・registry_a.json["tarot"] 縺九ｉ隱ｭ縺ｿ霎ｼ縺ｿ縲・
    繧ｱ繝ｫ繝亥香蟄励せ繝励Ξ繝・ラ・・0譫夲ｼ峨ｒ螻暮幕縺吶ｋ縲・
    """

    @lru_cache(maxsize=1)
    def _load_cards(self) -> list[dict]:
        registry = load_registry()
        cards = registry["tarot"]
        if len(cards) != 78:
            raise ValueError(f"registry_a.json 縺ｮ tarot 縺・{len(cards)} 譫壹〒縺吶・8 譫壹〒縺ゅｋ蠢・ｦ√′縺ゅｊ縺ｾ縺吶・)
        return cards

    def __init__(self) -> None:
        self._cards = self._load_cards()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def draw_celtic_cross(
        self,
        user_seed: int,
        query: str = "",
    ) -> dict:
        rng = random.Random(user_seed)

        # 78 譫壹ｒ繧ｷ繝｣繝・ヵ繝ｫ縺励※蜈磯ｭ 10 譫壹ｒ菴ｿ縺・
        deck_indices = list(range(len(self._cards)))
        rng.shuffle(deck_indices)
        drawn_indices = deck_indices[:10]

        # 豁｣騾・・繧ｷ繝ｼ繝峨↓蝓ｺ縺･縺・※迢ｬ遶九＠縺ｦ豎ｺ螳・
        reversed_flags = [rng.random() < 0.35 for _ in range(10)]

        positions: dict[str, dict] = {}
        for i, (pos_key, pos_label) in enumerate(CELTIC_CROSS_POSITIONS):
            card = self._cards[drawn_indices[i]]
            positions[pos_key] = {
                "position_label": pos_label,
                "position_index": i + 1,
                "card":           card,
                "is_reversed":    reversed_flags[i],
            }

        return {
            "query":     query,
            "seed":      user_seed,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "spread":    "celtic_cross",
            "positions": positions,
        }

    # ------------------------------------------------------------------
    # Utility
    # ------------------------------------------------------------------

    def all_cards(self) -> list[dict]:
        return list(self._cards)

    def card_count(self) -> int:
        return len(self._cards)
