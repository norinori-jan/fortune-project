#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
LopanRenderer.py

LopanModel を SVG へ描画する

入力:
    LopanModel

出力:
    lopan.svg
"""

import math
from pathlib import Path


class LopanRenderer:

    # =====================================================
    # 初期化
    # =====================================================

    def __init__(self, model):

        self.model = model

        self.size = 1200
        self.center = self.size / 2

        self.svg = []

    # =====================================================
    # SVG開始
    # =====================================================

    def begin_svg(self):

        self.svg.append('<?xml version="1.0" encoding="UTF-8"?>')

        self.svg.append(
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{self.size}" '
            f'height="{self.size}" '
            f'viewBox="0 0 {self.size} {self.size}">'
        )

        self.svg.append(
            '<rect width="100%" height="100%" fill="white"/>'
        )

    # =====================================================
    # SVG終了
    # =====================================================

    def end_svg(self):

        self.svg.append("</svg>")

    # =====================================================
    # 円
    # =====================================================

    def draw_circle(
        self,
        radius,
        stroke="black",
        stroke_width=1,
        fill="none"
    ):

        self.svg.append(
            f'<circle '
            f'cx="{self.center}" '
            f'cy="{self.center}" '
            f'r="{radius}" '
            f'stroke="{stroke}" '
            f'stroke-width="{stroke_width}" '
            f'fill="{fill}"/>'
        )

    # =====================================================
    # 線
    # =====================================================

    def draw_line(
        self,
        x1,
        y1,
        x2,
        y2,
        stroke="black",
        width=1
    ):

        self.svg.append(
            f'<line '
            f'x1="{x1}" '
            f'y1="{y1}" '
            f'x2="{x2}" '
            f'y2="{y2}" '
            f'stroke="{stroke}" '
            f'stroke-width="{width}"/>'
        )

    # =====================================================
    # テキスト
    # =====================================================

    def draw_text(
        self,
        x,
        y,
        text,
        size=12
    ):

        self.svg.append(
            f'<text '
            f'x="{x}" '
            f'y="{y}" '
            f'font-size="{size}" '
            f'text-anchor="middle" '
            f'dominant-baseline="middle">'
            f'{text}'
            f'</text>'
        )

    # =====================================================
    # Layer01
    # =====================================================

    def draw_layer01(self):

        print("Draw Layer01")

        # 後で実装

        pass

    # =====================================================
    # Layer23
    # =====================================================

    def draw_layer23(self):

        print("Draw Layer23")

        # 後で実装

        pass

    # =====================================================
    # Layer24
    # =====================================================

    def draw_layer24(self):

        print("Draw Layer24")

        # 後で実装

        pass

    # =====================================================
    # 描画
    # =====================================================

    def render(self):

        self.begin_svg()

        self.draw_circle(500)

        self.draw_layer01()

        self.draw_layer23()

        self.draw_layer24()

        self.end_svg()

    # =====================================================
    # 保存
    # =====================================================

    def save(self, filename):

        Path(filename).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(filename, "w", encoding="utf-8") as f:

            f.write("\n".join(self.svg))

        print("Saved:", filename)