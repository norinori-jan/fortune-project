#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
main.py

羅盤SVG生成

実行

python main.py

↓

output/lopan.svg
"""

from pathlib import Path

from LopanLoader import LopanLoader
from LopanRenderer import LopanRenderer


# =====================================================
# Main
# =====================================================

def main():

    json_file = (
        Path(__file__).parent
        / "data"
        / "master"
        / "lopan_master.json"
    )

    print("--------------------------------")
    print("Loading Master")
    print("--------------------------------")

    loader = LopanLoader(json_file)

    model = loader.load()

    print()

    print("--------------------------------")
    print("Rendering SVG")
    print("--------------------------------")

    renderer = LopanRenderer(model)

    output = (
        Path(__file__).parent
        / "output"
        / "lopan.svg"
    )

    renderer.save(output)

    print()

    print("--------------------------------")
    print("Finished")
    print("--------------------------------")


# =====================================================

if __name__ == "__main__":
    main()
