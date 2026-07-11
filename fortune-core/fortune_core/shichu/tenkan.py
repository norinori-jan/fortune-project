from core.registry_loader import load_registry

from ..pillar import Pillar

REGISTRY = load_registry()

STEMS = REGISTRY["stems"]
BRANCHES = REGISTRY["branches"]