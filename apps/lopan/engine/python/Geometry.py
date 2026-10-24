#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Geometry.py

羅盤描画用 幾何ライブラリ

機能
------
・角度→ラジアン
・角度→XY座標
・中間角
・角度幅
・距離
・円弧Path生成
・扇形Path生成
・文字配置座標
"""

import math


class Geometry:

    # =====================================================
    # Degree → Radian
    # =====================================================

    @staticmethod
    def deg2rad(angle: float) -> float:
        return math.radians(angle)

    # =====================================================
    # Normalize
    # =====================================================

    @staticmethod
    def normalize(angle: float) -> float:
        angle %= 360.0
        if angle < 0:
            angle += 360.0
        return angle

    # =====================================================
    # Polar → Cartesian
    #
    # SVGは12時方向を0°
    # =====================================================

    @staticmethod
    def polar(radius: float,
              angle: float):

        rad = math.radians(angle - 90)

        x = radius * math.cos(rad)
        y = radius * math.sin(rad)

        return x, y

    # =====================================================
    # Distance
    # =====================================================

    @staticmethod
    def distance(x1,
                 y1,
                 x2,
                 y2):

        return math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

    # =====================================================
    # Angle Width
    # =====================================================

    @staticmethod
    def sweep(start_angle,
              end_angle):

        if end_angle < start_angle:
            end_angle += 360

        return end_angle - start_angle

    # =====================================================
    # Middle Angle
    # =====================================================

    @staticmethod
    def middle_angle(start_angle,
                     end_angle):

        if end_angle < start_angle:
            end_angle += 360

        return (start_angle + end_angle) / 2 % 360

    # =====================================================
    # Text Position
    # =====================================================

    @staticmethod
    def text_position(radius,
                      start_angle,
                      end_angle):

        angle = Geometry.middle_angle(
            start_angle,
            end_angle
        )

        return Geometry.polar(radius, angle)

    # =====================================================
    # Circle Arc SVG Path
    # =====================================================

    @staticmethod
    def arc(radius,
            start_angle,
            end_angle):

        x1, y1 = Geometry.polar(radius, start_angle)
        x2, y2 = Geometry.polar(radius, end_angle)

        large_arc = 0

        if Geometry.sweep(start_angle, end_angle) > 180:
            large_arc = 1

        return (
            f"M {x1:.3f},{y1:.3f} "
            f"A {radius:.3f},{radius:.3f} "
            f"0 {large_arc} 1 "
            f"{x2:.3f},{y2:.3f}"
        )

    # =====================================================
    # Sector SVG Path
    # =====================================================

    @staticmethod
    def sector(inner_radius,
               outer_radius,
               start_angle,
               end_angle):

        x1, y1 = Geometry.polar(
            outer_radius,
            start_angle
        )

        x2, y2 = Geometry.polar(
            outer_radius,
            end_angle
        )

        x3, y3 = Geometry.polar(
            inner_radius,
            end_angle
        )

        x4, y4 = Geometry.polar(
            inner_radius,
            start_angle
        )

        large_arc = 0

        if Geometry.sweep(start_angle, end_angle) > 180:
            large_arc = 1

        return (
            f"M {x1:.3f},{y1:.3f} "
            f"A {outer_radius:.3f},{outer_radius:.3f} "
            f"0 {large_arc} 1 "
            f"{x2:.3f},{y2:.3f} "
            f"L {x3:.3f},{y3:.3f} "
            f"A {inner_radius:.3f},{inner_radius:.3f} "
            f"0 {large_arc} 0 "
            f"{x4:.3f},{y4:.3f} "
            f"Z"
        )

    # =====================================================
    # Line
    # =====================================================

    @staticmethod
    def line(inner_radius,
             outer_radius,
             angle):

        x1, y1 = Geometry.polar(
            inner_radius,
            angle
        )

        x2, y2 = Geometry.polar(
            outer_radius,
            angle
        )

        return (
            f"M {x1:.3f},{y1:.3f} "
            f"L {x2:.3f},{y2:.3f}"
        )

    # =====================================================
    # Circle
    # =====================================================

    @staticmethod
    def circle(radius):

        return (
            f'<circle cx="0" cy="0" '
            f'r="{radius:.3f}" '
            f'fill="none"/>'
        )
        