# fortune_core/iching/registry_loader.py

import json
from pathlib import Path


class RegistryLoader:
    """
    易経レジストリ読込
    """

    def __init__(self):

        root = (
            Path(__file__)
            .resolve()
            .parents[3]
            / "fortune-registry"
            / "iching"
        )

        self.root = root

    def _load(self, filename):

        path = self.root / filename

        with open(
            path,
            encoding="utf-8",
        ) as f:

            return json.load(f)

    def get_trigrams(self):

        return self._load("trigrams.json")

    def get_hexagrams(self):

        return self._load("hexagrams.json")

    def get_judgement(self):

        return self._load("judgement.json")

    def get_image(self):

        return self._load("image.json")

    def get_yao(self):

        return self._load("yao.json")