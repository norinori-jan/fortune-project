from __future__ import annotations

from functools import lru_cache
from .registry_loader import load_registry


@lru_cache(maxsize=1)
def _load_hexagrams() -> list[dict]:
    """
    SSOT（Single Source of Truth）として registry_loader が読み込む
    registry_a.json から六十四卦データを取得する
    """
    registry = load_registry()
    return registry["hexagrams"]


def get_hexagram(hexagram_id: int) -> dict:
    hexagrams = _load_hexagrams()
    for hexagram in hexagrams:
        if hexagram.get("id") == hexagram_id:
            return hexagram
    raise ValueError(f"Unknown hexagram id: {hexagram_id}")


def get_trigram(trigram_id: int) -> dict:
    # Deprecated: Use get_hexagram instead.
    return get_hexagram(trigram_id)
