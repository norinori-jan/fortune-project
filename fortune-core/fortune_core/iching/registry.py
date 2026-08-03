from __future__ import annotations

from .registry_loader import RegistryLoader


class Registry:
    """
    I Ching Registry Access
    """

    def __init__(self) -> None:
        self._loader = RegistryLoader()

    @property
    def hexagrams(self):
        return self._loader.hexagrams

    @property
    def judgement(self):
        return self._loader.judgement

    @property
    def image(self):
        return self._loader.image

    @property
    def yao(self):
        return self._loader.yao