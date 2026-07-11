from pathlib import Path
import json

# fortune-project/
ROOT = Path(__file__).resolve().parents[2]

# fortune-project/fortune-registry/shichu/
BASE = ROOT / "fortune-registry" / "shichu"


def _load(filename: str):
    with open(BASE / filename, encoding="utf-8-sig") as f:
        return json.load(f)


def load_registry():
    return {
        "stems": _load("stems.json"),
        "branches": _load("branches.json"),
        "hidden_stems": _load("hidden_stems.json"),
        "sixty_kanchi": _load("sixty_kanchi.json"),
        "ten_gods": _load("ten_gods.json"),
        "twelve_growth": _load("twelve_growth.json"),
        "relations": _load("relations.json"),
        "solar_terms": _load("solar_terms.json"),
        "gods": _load("gods.json"),
    }