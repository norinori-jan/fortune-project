from __future__ import annotations

import random
from datetime import datetime, timezone
from functools import lru_cache
from .registry_loader import load_registry

# ---------------------------------------------------------------------------
# ポジション定義（挿入順序が展開順）
# ---------------------------------------------------------------------------
CELTIC_CROSS_POSITIONS: list[tuple[str, str]] = [
    ("CURRENT_SITUATION",   "現在の状況"),
    ("CROSSING_CHALLENGE",  "課題・交差するもの"),
    ("DISTANT_PAST",        "遠い過去・根底にあるもの"),
    ("RECENT_PAST",         "近い過去の影響"),
    ("BEST_OUTCOME",        "意識・最善の結果"),
    ("IMMEDIATE_FUTURE",    "近未来の方向性"),
    ("SELF_PERCEPTION",     "自己認識・内面"),
    ("EXTERNAL_INFLUENCES", "外部環境・他者の影響"),
    ("HOPES_AND_FEARS",     "希望と恐れ"),
    ("FINAL_OUTCOME",       "最終的な結末"),
]

# ---------------------------------------------------------------------------
# TarotEngine（SSOT版）
# ---------------------------------------------------------------------------

class TarotEngine:
    """
    タロットエンジン（SSOT: core/registry_a.json を参照）

    78 枚のフルデッキを registry_a.json["tarot"] から読み込み、
    ケルト十字スプレッド（10枚）を展開する。
    """

    @lru_cache(maxsize=1)
    def _load_cards(self) -> list[dict]:
        registry = load_registry()
        cards = registry["tarot"]
        if len(cards) != 78:
            raise ValueError(f"registry_a.json の tarot が {len(cards)} 枚です。78 枚である必要があります。")
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

        # 78 枚をシャッフルして先頭 10 枚を使う
        deck_indices = list(range(len(self._cards)))
        rng.shuffle(deck_indices)
        drawn_indices = deck_indices[:10]

        # 正逆はシードに基づいて独立して決定
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
