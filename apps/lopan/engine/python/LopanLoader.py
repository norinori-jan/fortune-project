#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LopanLoader.py

羅盤マスターJSONローダー
"""

import json
from pathlib import Path


class LopanLoader:

    def __init__(self, filename):

        self.filename = Path(filename)
        self.master = None

    # =====================================================
    # Load
    # =====================================================

    def load(self):

        with open(self.filename, encoding="utf-8") as f:
            self.master = json.load(f)

        return self.master

    # =====================================================
    # Metadata
    # =====================================================

    def metadata(self):

        return self.master["metadata"]

    # =====================================================
    # Layer
    # =====================================================

    def layer(self, layer_name):

        return self.master["layers"][layer_name]

    # =====================================================
    # Layer Names
    # =====================================================

    def layer_names(self):

        return list(self.master["layers"].keys())

    # =====================================================
    # Cell
    # =====================================================

    def get_cell(self, layer_name, index):

        layer = self.layer(layer_name)

        if index < 0 or index >= len(layer):
            return None

        return layer[index]

    # =====================================================
    # Angle Search
    # =====================================================

    def find_angle(self, layer_name, angle):

        angle = angle % 360.0

        layer = self.layer(layer_name)

        for cell in layer:

            start = cell["start_angle"]
            end = cell["end_angle"]

            # 通常区間
            if start < end:
                if start <= angle < end:
                    return cell

            # 360跨ぎ
            else:
                if angle >= start or angle < end:
                    return cell

        return None

    # =====================================================
    # Summary
    # =====================================================

    def summary(self):

        print("Metadata")
        print("----------------------")

        for k, v in self.metadata().items():
            print(f"{k:20}: {v}")

        print()

        print("Layers")
        print("----------------------")

        for name in self.layer_names():

            print(f"{name:10} {len(self.layer(name))} items")

