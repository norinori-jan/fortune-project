"""
registry_loader.py — registry_a.json の shichu セクションをロードしてキャッシュする
"""
import json
import os
from pathlib import Path

_REGISTRY_CACHE = None

def get_registry() -> dict:
    global _REGISTRY_CACHE
    if _REGISTRY_CACHE is not None:
        return _REGISTRY_CACHE

    candidates = []
    env_path = os.environ.get("REGISTRY_PATH")
    if env_path:
        candidates.append(Path(env_path))

    base = Path(__file__).resolve().parent.parent / "registry_a.json"
    candidates.append(base)
    candidates.append(Path("registry_a.json"))

    for path in candidates:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            _REGISTRY_CACHE = data.get("shichu", data)
            return _REGISTRY_CACHE

    raise FileNotFoundError(
        "registry_a.json が見つかりません。"
        "REGISTRY_PATH 環境変数を設定するか、core/ に置いてください。"
    )

def clear_cache():
    global _REGISTRY_CACHE
    _REGISTRY_CACHE = None
