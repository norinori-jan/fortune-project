
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LopanModel.py

LopanLoader が読み込んだ JSON を
Pythonオブジェクトへ変換する
"""

from dataclasses import dataclass
from typing import List


# ==========================================================
# Layer01
# ==========================================================

@dataclass
class Fixed64Sector:

    id: int
    index: int

    start_angle: float
    end_angle: float
    width: float

    ganchu: str
    kyusei: str
    unsu: str
    kokei: str


# ==========================================================
# Layer23
# ==========================================================

@dataclass
class HostSector:

    id: int
    index: int

    start_angle: float
    end_angle: float
    width: float

    host: str


# ==========================================================
# Layer24
# ==========================================================

@dataclass
class TermSector:

    id: int
    index: int

    start_angle: float
    end_angle: float
    width: float

    term: str


# ==========================================================
# LopanModel
# ==========================================================

class LopanModel:

    def __init__(self, master):

        self.metadata = master["metadata"]

        self.layer01 = self._build_fixed64(
            master["layers"]["layer01"]
        )

        self.layer23 = self._build_hosts(
            master["layers"]["layer23"]
        )

        self.layer24 = self._build_terms(
            master["layers"]["layer24"]
        )

    # ------------------------------------------------------

    def _build_fixed64(self, data):

        result: List[Fixed64Sector] = []

        for item in data:

            result.append(

                Fixed64Sector(

                    id=item["id"],
                    index=item["index"],

                    start_angle=item["start_angle"],
                    end_angle=item["end_angle"],
                    width=item["width"],

                    ganchu=item["ganchu"],
                    kyusei=item["kyusei"],
                    unsu=item["unsu"],
                    kokei=item["kokei"]

                )

            )

        return result

    # ------------------------------------------------------

    def _build_hosts(self, data):

        result: List[HostSector] = []

        for item in data:

            result.append(

                HostSector(

                    id=item["id"],
                    index=item["index"],

                    start_angle=item["start_angle"],
                    end_angle=item["end_angle"],
                    width=item["width"],

                    host=item["host"]

                )

            )

        return result

    # ------------------------------------------------------

    def _build_terms(self, data):

        result: List[TermSector] = []

        for item in data:

            result.append(

                TermSector(

                    id=item["id"],
                    index=item["index"],

                    start_angle=item["start_angle"],
                    end_angle=item["end_angle"],
                    width=item["width"],

                    term=item["term"]

                )

            )

        return result