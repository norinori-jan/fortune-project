import math


# ==========================================================
# Angle
# ==========================================================

def normalize(angle):
    """
    角度を 0〜360°へ正規化
    """

    return angle % 360


# ==========================================================
# Degree → Radian
# ==========================================================

def deg_to_rad(angle_deg):
    """
    度 → ラジアン
    """

    return math.radians(angle_deg)


# ==========================================================
# Polar → Cartesian
# ==========================================================

def polar_to_cartesian(
    cx,
    cy,
    radius,
    angle_deg,
):
    """
    極座標をSVG座標へ変換
    """

    angle = math.radians(angle_deg - 90)

    x = cx + radius * math.cos(angle)
    y = cy + radius * math.sin(angle)

    return x, y


# ==========================================================
# SVG Arc
# ==========================================================

def arc_path(
    cx,
    cy,
    radius,
    start_deg,
    end_deg,
):
    """
    SVG円弧パス
    """

    x1, y1 = polar_to_cartesian(
        cx,
        cy,
        radius,
        start_deg,
    )

    x2, y2 = polar_to_cartesian(
        cx,
        cy,
        radius,
        end_deg,
    )

    large_arc = 1 if (end_deg - start_deg) > 180 else 0

    return (
        f"M {x1:.2f},{y1:.2f} "
        f"A {radius},{radius} 0 {large_arc} 1 "
        f"{x2:.2f},{y2:.2f}"
    )


# ==========================================================
# SVG Ring Sector
# ==========================================================

def ring_sector(
    cx,
    cy,
    inner_radius,
    outer_radius,
    start_deg,
    end_deg,
):
    """
    ドーナツ状扇形パスを生成
    """

    outer = arc_path(
        cx,
        cy,
        outer_radius,
        start_deg,
        end_deg,
    )

    inner = arc_path(
        cx,
        cy,
        inner_radius,
        end_deg,
        start_deg,
    )

    x1, y1 = polar_to_cartesian(
        cx,
        cy,
        inner_radius,
        start_deg,
    )

    return (
        f"{outer} "
        f"L {x1:.2f},{y1:.2f} "
        f"{inner} Z"
    )


# ==========================================================
# SVG Text Position
# ==========================================================

def text_position(
    cx,
    cy,
    radius,
    angle_deg,
):
    """
    SVG文字配置座標
    """

    return polar_to_cartesian(
        cx,
        cy,
        radius,
        angle_deg,
    )