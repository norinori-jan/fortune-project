from pathlib import Path
import json

from .stems import Stem
from .branches import Branch


class RegistryLoader:
    """
    fortune-registry の JSON を読み込み、
    Engine が利用するオブジェクトへ変換する。
    """

    def __init__(self, base_path: str):
        self.base = Path(base_path)
        self.shichu = self.base / "shichu"

        self._stems = self._load(self.shichu / "stems.json")
        self._branches = self._load(self.shichu / "branches.json")
        self._hidden_stems = self._load(self.shichu / "hidden_stems.json")
        self._sixty_kanchi = self._load(self.shichu / "sixty_kanchi.json")
        self._ten_gods = self._load(self.shichu / "ten_gods.json")
        self._twelve_growth = self._load(self.shichu / "twelve_growth.json")
        self._relations = self._load(self.shichu / "relations.json")
        self._gods = self._load(self.shichu / "gods.json")

    def _load(self, path: Path):
        with open(path, "r", encoding="utf-8-sig") as f:
            return json.load(f)

    # -------------------------
    # Stem
    # -------------------------
    def get_stems(self):
        result = {}

        for k, v in self._stems.items():

            result[k] = Stem(
                name=v["name"],
                element=v.get("element", v.get("five_elements")),
                yin_yang=v["yin_yang"],
                index=v["index"]
            )

        return result
    # -------------------------
    # Branch
    # -------------------------
    def get_branches(self):
        result = {}

        for key, value in self._branches.items():
            result[key] = Branch(
                name=value["name"],
                index=value["index"],
                yin_yang=value["yin_yang"],
                element=value.get("five_elements"),
                hidden_stems=value.get("hidden_stems", []),
            )

        return result

    # -------------------------
    # その他
    # -------------------------
    def get_hidden_stems(self):
        return self._hidden_stems

    def get_sixty_kanchi(self):
        return self._sixty_kanchi

    def get_ten_gods(self):
        return self._ten_gods

    def get_twelve_growth(self):
        return self._twelve_growth

    def get_relations(self):
        return self._relations

    
    def get_gods(self):
        return self._gods