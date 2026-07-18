# fortune_core/iching/registry_loader.py

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class RegistryLoader:
    """
    易経レジストリ読み込みクラス

    fortune-registry/
        iching/
            trigrams.json
            hexagrams.json
            judgement.json
            image.json
            yao.json
    """

    def __init__(self, registry_root: Path | None = None):

        if registry_root is None:

            registry_root = (
                Path(__file__)
                .resolve()
                .parents[3]
                / "fortune-registry"
                / "iching"
            )

        self.registry_root = registry_root

    # ---------------------------------------------------------
    # 共通JSON読込
    # ---------------------------------------------------------

    def _load_json(self, filename: str) -> Any:

        path = self.registry_root / filename

        if not path.exists():

            raise FileNotFoundError(
                f"Registry file not found: {path}"
            )

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as f:

            return json.load(f)

    # ---------------------------------------------------------
    # 八卦
    # ---------------------------------------------------------

    def load_trigrams(self):

        return self._load_json(
            "trigrams.json"
        )

    # ---------------------------------------------------------
    # 六十四卦
    # ---------------------------------------------------------

    def load_hexagrams(self):

        return self._load_json(
            "hexagrams.json"
        )

    # ---------------------------------------------------------
    # 卦辞
    # ---------------------------------------------------------

    def load_judgements(self):

        return self._load_json(
            "judgement.json"
        )

    # ---------------------------------------------------------
    # 象伝
    # ---------------------------------------------------------

    def load_images(self):

        return self._load_json(
            "image.json"
        )

    # ---------------------------------------------------------
    # 爻辞
    # ---------------------------------------------------------

    def load_yao(self):

        return self._load_json(
            "yao.json"
        )