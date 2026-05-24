import json
from pathlib import Path

def load_registry():
    core_path = Path(__file__).resolve().parents[3] / "core" / "registry_a.json"
    with open(core_path, "r", encoding="utf-8") as f:
        return json.load(f)
