from pathlib import Path
import json


class RegistryLoader:
    """
    fortune-registry の JSON を読み込み、
    Engine / TenkanEngine / ZangKanEngine が必要とする
    get_stems(), get_branches(), get_hidden_stems() などの
    API を提供するクラス。
    """

    def __init__(self, base_path: str):
        self.base = Path(base_path)

        # shichu ディレクトリ
        self.shichu = self.base / "shichu"

        # common ディレクトリ
        self.common = self.base / "common"

        # すべて UTF-8 BOM 対応
        self._stems = self._load(self.common / "stems.json")
        self._branches = self._load(self.common / "branches.json")
        self._hidden_stems = self._load(self.shichu / "hidden_stems.json")
        self._sixty_kanchi = self._load(self.shichu / "sixty_kanchi.json")
        self._ten_gods = self._load(self.shichu / "ten_gods.json")
        self._twelve_growth = self._load(self.shichu / "twelve_growth.json")
        self._relations = self._load(self.shichu / "relations.json")
        self._solar_terms = self._load(self.shichu / "solar_terms.json")
        self._gods = self._load(self.shichu / "gods.json")

    def _load(self, path: Path):
        with open(path, encoding="utf-8-sig") as f:
            return json.load(f)

    # -------------------------
    # Engine が要求する API
    # -------------------------
    def get_stems(self):
        return self._stems

    def get_branches(self):
        return self._branches

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

    def get_solar_terms(self):
        return self._solar_terms

    def get_gods(self):
        return self._gods
