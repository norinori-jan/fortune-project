#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_master.py

羅盤マスターデータ生成

生成先
    data/master/lopan_master.json

構成
    Layer01  固定64区画
    Layer02  八卦
    Layer03  地盤二十四山
    Layer04  天盤二十四山
    Layer05  人盤二十四山
    Layer06  透地六十龍
    Layer07  百二十分金
    Layer08
    Layer09
    Layer10
    Layer11
    Layer12
    Layer13  二十八宿
    Layer14  二十四節気
    Layer15
    Layer16
    Layer17
    Layer18
    Layer19
    Layer20
    Layer21
    Layer22
    Layer23
    Layer24
    Layer25
    Layer26

設計方針

・全レイヤは create_xxx_layer() で生成
・角度はすべて Degree
・JSONのみを出力
・CSVは将来データソースとして利用可能
"""

import json
import math
from pathlib import Path

# ==========================================================
# 基本定数
# ==========================================================

FULL_CIRCLE = 360.0

# Layer01（固定64区画）
FIXED64_DIVISIONS = 64
FIXED64_WIDTH = FULL_CIRCLE / FIXED64_DIVISIONS

# 基準位置
ANCHOR_INDEX = 13
ANCHOR_START = 15.0

BASE_START = ANCHOR_START - ANCHOR_INDEX * FIXED64_WIDTH

# ==========================================================
# 共通関数
# ==========================================================

def normalize(angle):
    """
    角度を 0～360° に正規化する
    """

    if abs(angle - 360.0) < 1e-9:
        return 360.0

    angle = angle % 360.0

    if abs(angle - 360.0) < 1e-9:
        return 360.0

    return angle

def angle_width(start, end):
    """
    開始角・終了角から幅を求める
    """

    if end >= start:
        return end - start

    return (360.0 - start) + end

def create_angle_record(
    index,
    start,
    end,
    **kwargs
):
    """
    全Layer共通フォーマット
    """

    record = {

        "id": index,

        "start_angle": round(normalize(start), 6),

        "end_angle": round(normalize(end), 6),

        "width": round(angle_width(start, end), 6)

    }

    record.update(kwargs)

    return record

entries = [

    ("丁亥", "天輔", "カ8上", "無〇無無〇無"),
    ("己亥", "天巨", "カ2上", "〇〇無〇〇無"),
    ("辛亥", "人破", "上7カ", "無無〇無無〇"),
    ("癸亥", "地武", "カ6上", "上〇無上〇無"),
    ("甲子", "父貪", "上1カ", "〇無無〇無無"),
    ("甲子", "天輔", "カ9上", "無〇無無〇無"),
    ("丙子", "人禄", "上3カ", "無〇〇無〇〇"),
    ("戊子", "地文", "カ4上", "無無〇無無〇"),
    ("庚子", "母弼", "上9カ", "〇無無〇無無"),
    ("壬子", "父貪", "上1カ", "〇無無〇無無"),
    ("乙丑", "地武", "カ6上", "上〇無上〇無"),
    ("丁丑", "人破", "上7カ", "無無〇無無〇"),
    ("己丑", "天巨", "カ2上", "〇〇無〇〇無"),
    ("辛丑", "人禄", "上3カ", "無〇〇無〇〇"),
    ("癸丑", "天輔", "カ8上", "無〇無無〇無"),
    ("甲寅", "母弼", "上9カ", "〇無無〇無無"),
    ("丙寅", "地文", "カ4上", "無無〇無無〇"),
    ("戊寅", "地武", "カ6上", "上〇無上〇無"),
    ("庚寅", "父貪", "上1カ", "〇無無〇無無"),
    ("庚寅", "天巨", "カ2上", "〇〇無〇〇無"),
    ("壬寅", "人破", "上7カ", "無無〇無無〇"),
    ("乙卯", "地文", "カ4上", "無無〇無無〇"),
    ("丁卯", "母弼", "上9カ", "〇無無〇無無"),
    ("己卯", "天輔", "カ8上", "無〇無無〇無"),
    ("辛卯", "人禄", "上3カ", "無〇〇無〇〇"),
    ("癸卯", "人破", "上7カ", "無無〇無無〇"),
    ("甲辰", "天巨", "カ2上", "〇〇無〇〇無"),
    ("丙辰", "父貪", "上1カ", "〇無無〇無無"),
    ("戊辰", "地武", "カ6上", "上〇無上〇無"),
    ("庚辰", "母弼", "上9カ", "〇無無〇無無"),
    ("壬辰", "地文", "カ4上", "無無〇無無〇"),
    ("乙巳", "人禄", "上3カ", "無〇〇無〇〇"),
    ("丁巳", "天輔", "カ8上", "無〇無無〇無"),
    ("己巳", "天巨", "カ2上", "〇〇無〇〇無"),
    ("辛巳", "人破", "上7カ", "無無〇無無〇"),
    ("癸巳", "地武", "カ6上", "上〇無上〇無"),
    ("甲午", "父貪", "上1カ", "〇無無〇無無"),
    ("甲午", "天輔", "カ8上", "無〇無無〇無"),
    ("丙午", "人禄", "上3カ", "無〇〇無〇〇"),
    ("戊午", "地文", "カ4上", "無無〇無無〇"),
    ("庚午", "母弼", "上9カ", "〇無無〇無無"),
    ("壬午", "父貪", "上1カ", "〇無無〇無無"),
    ("乙未", "地武", "カ6上", "上〇無上〇無"),
    ("丁未", "人破", "上7カ", "無無〇無無〇"),
    ("己未", "天巨", "カ2上", "〇〇無〇〇無"),
    ("辛未", "人禄", "上3カ", "無〇〇無〇〇"),
    ("癸未", "天輔", "カ8上", "無〇無無〇無"),
    ("甲申", "母弼", "上9カ", "〇無無〇無無"),
    ("丙申", "地文", "カ4上", "無無〇無無〇"),
    ("戊申", "地武", "カ6上", "上〇無上〇無"),
    ("庚申", "父貪", "上1カ", "〇無無〇無無"),
    ("庚申", "天巨", "カ2上", "〇〇無〇〇無"),
    ("壬申", "人破", "上7カ", "無〇無無〇無"),
    ("乙酉", "地文", "カ4上", "無無〇無無〇"),
    ("丁酉", "母弼", "上9カ", "〇無無〇無無"),
    ("己酉", "天輔", "カ8上", "無〇無無〇無"),
    ("辛酉", "人禄", "上3カ", "無〇〇無〇〇"),
    ("癸酉", "人破", "上7カ", "無無〇無無〇"),
    ("甲戌", "天巨", "カ2上", "〇〇無〇〇無"),
    ("丙戌", "父貪", "上1カ", "〇無無〇無無"),
    ("戊戌", "地武", "カ6上", "上〇無上〇無"),
    ("庚戌", "母弼", "上9カ", "〇無無〇無無"),
    ("壬戌", "地文", "カ4上", "無無〇無無〇"),
    ("乙亥", "人禄", "上3カ", "無〇〇無〇〇"),

]

def create_fixed64_layer():
    """
    Layer01 固定64区画
    """

    layer = []

    for index, (ganchu, kyusei, kaun, kokei) in enumerate(entries):

        start = BASE_START + index * FIXED64_WIDTH
        end = start + FIXED64_WIDTH

        layer.append(

            create_angle_record(

                index=index + 1,

                start=start,

                end=end,

                ganchu=ganchu,

                kyusei=kyusei,

                kaun=kaun,

                kokei=kokei

            )

        )

    return layer

# ==========================================================
# Layer02 : 八卦
# ==========================================================

bagua = [

    ("乾",   0.0,   45.0),
    ("兌",  45.0,   90.0),
    ("離",  90.0,  135.0),
    ("震", 135.0,  180.0),
    ("巽", 180.0,  225.0),
    ("坎", 225.0,  270.0),
    ("艮", 270.0,  315.0),
    ("坤", 315.0,  360.0),

]

def create_bagua_layer():
    """
    Layer02 八卦
    """

    layer = []

    for index, (name, start, end) in enumerate(bagua, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                bagua=name

            )

        )

    return layer

# ==========================================================
# Layer03 : 地盤二十四山
# ==========================================================

direction24 = [

    ("子",   0.0,  15.0),
    ("癸",  15.0,  30.0),
    ("丑",  30.0,  45.0),
    ("艮",  45.0,  60.0),
    ("寅",  60.0,  75.0),
    ("甲",  75.0,  90.0),
    ("卯",  90.0, 105.0),
    ("乙", 105.0, 120.0),
    ("辰", 120.0, 135.0),
    ("巽", 135.0, 150.0),
    ("巳", 150.0, 165.0),
    ("丙", 165.0, 180.0),
    ("午", 180.0, 195.0),
    ("丁", 195.0, 210.0),
    ("未", 210.0, 225.0),
    ("坤", 225.0, 240.0),
    ("申", 240.0, 255.0),
    ("庚", 255.0, 270.0),
    ("酉", 270.0, 285.0),
    ("辛", 285.0, 300.0),
    ("戌", 300.0, 315.0),
    ("乾", 315.0, 330.0),
    ("亥", 330.0, 345.0),
    ("壬", 345.0, 360.0),

]


def create_direction24_layer():
    """
    Layer03 地盤二十四山
    """

    layer = []

    for index, (name, start, end) in enumerate(direction24, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                direction=name,

                plane="earth"

            )

        )

    return layer
    # ==========================================================
# Layer04 : 天盤二十四山
# ==========================================================

def create_heaven24_layer():
    """
    Layer04 天盤二十四山（+7.5°）
    """

    layer = []

    OFFSET = 7.5

    for index, (name, start, end) in enumerate(direction24, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start + OFFSET,

                end=end + OFFSET,

                direction=name,

                plane="heaven"

            )

        )

    return layer

# ==========================================================
# Layer05 : 人盤二十四山
# ==========================================================

def create_human24_layer():
    """
    Layer05 人盤二十四山（+15.0°）
    """

    layer = []

    OFFSET = 15.0

    for index, (name, start, end) in enumerate(direction24, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start + OFFSET,

                end=end + OFFSET,

                direction=name,

                plane="human"

            )

        )

    return layer

# 

# ==========================================================
# Layer06 : 透地六十龍
# ==========================================================

dragon60 = [

    # 子山
    ("甲子",   0.0,   6.0),
    ("丙子",   6.0,  12.0),
    ("戊子",  12.0,  18.0),
    ...
    ("癸亥", 354.0, 360.0),

]

def create_dragon60_layer():
    """
    Layer06 : 透地六十龍
    """

    layer = []

    for index, (name, start, end) in enumerate(dragon60, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                dragon=name

            )

        )

    return layer

# ==========================================================
# Layer07 : 百二十分金
# ==========================================================

# ※ 現在は規則生成
# ※ 将来は実測CSVへ置き換え可能

gold120 = []

branches = [
    "子", "丑", "寅", "卯", "辰", "巳",
    "午", "未", "申", "酉", "戌", "亥"
]

stems = [
    "甲", "乙", "丙", "丁", "戊",
    "己", "庚", "辛", "壬", "癸"
]

index = 0

for branch in branches:

    for stem in stems:

        start = index * 3.0
        end = start + 3.0

        gold120.append(
            (
                f"{stem}{branch}",
                start,
                end
            )
        )

        index += 1


def create_gold120_layer():
    """
    Layer07 百二十分金
    """

    layer = []

    for index, (name, start, end) in enumerate(gold120, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                gold=name

            )

        )

    return layer

# ==========================================================
# Layer08 : 二十八宿
# ==========================================================

# ※ 現在は実測データを直接定義
# ※ 将来はCSVから読み込む予定

hosts28 = [

    # ("角", start, end),
    # ("亢", start, end),
    # ("氐", start, end),
    # ("房", start, end),
    # ("心", start, end),
    # ("尾", start, end),
    # ("箕", start, end),
    # ("斗", start, end),
    # ("牛", start, end),
    # ("女", start, end),
    # ("虚", start, end),
    # ("危", start, end),
    # ("室", start, end),
    # ("壁", start, end),
    # ("奎", start, end),
    # ("婁", start, end),
    # ("胃", start, end),
    # ("昴", start, end),
    # ("畢", start, end),
    # ("觜", start, end),
    # ("参", start, end),
    # ("井", start, end),
    # ("鬼", start, end),
    # ("柳", start, end),
    # ("星", start, end),
    # ("張", start, end),
    # ("翼", start, end),
    # ("軫", start, end),

]


def create_host_layer():
    """
    Layer08 : 二十八宿
    """

    layer = []

    for index, (name, start, end) in enumerate(hosts28, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                host=name

            )

        )

    return layer

==========================================================
# Layer09 : 二十四節気
# ==========================================================

solar_terms = [

    ("立春",    0.0,   15.0),
    ("雨水",   15.0,   30.0),
    ("啓蟄",   30.0,   45.0),
    ("春分",   45.0,   60.0),
    ("清明",   60.0,   75.0),
    ("穀雨",   75.0,   90.0),

    ("立夏",   90.0,  105.0),
    ("小満",  105.0,  120.0),
    ("芒種",  120.0,  135.0),
    ("夏至",  135.0,  150.0),
    ("小暑",  150.0,  165.0),
    ("大暑",  165.0,  180.0),

    ("立秋",  180.0,  195.0),
    ("処暑",  195.0,  210.0),
    ("白露",  210.0,  225.0),
    ("秋分",  225.0,  240.0),
    ("寒露",  240.0,  255.0),
    ("霜降",  255.0,  270.0),

    ("立冬",  270.0,  285.0),
    ("小雪",  285.0,  300.0),
    ("大雪",  300.0,  315.0),
    ("冬至",  315.0,  330.0),
    ("小寒",  330.0,  345.0),
    ("大寒",  345.0,  360.0),

]


def create_solar_term_layer():
    """
    Layer09 : 二十四節気
    """

    layer = []

    for index, (name, start, end) in enumerate(solar_terms, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                solar_term=name

            )

        )

    return layer


# ==========================================================
# Layer10 : 十天干
# ==========================================================

heavenly_stems = [

    ("甲",   0.0,   36.0),
    ("乙",  36.0,   72.0),
    ("丙",  72.0,  108.0),
    ("丁", 108.0,  144.0),
    ("戊", 144.0,  180.0),

    ("己", 180.0,  216.0),
    ("庚", 216.0,  252.0),
    ("辛", 252.0,  288.0),
    ("壬", 288.0,  324.0),
    ("癸", 324.0,  360.0),

]


def create_stem_layer():
    """
    Layer10 : 十天干
    """

    layer = []

    for index, (name, start, end) in enumerate(heavenly_stems, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                stem=name

            )

        )

    return layer

# ==========================================================
# Layer10 : 十天干
# ==========================================================

heavenly_stems = [

    ("甲",   0.0,   36.0),
    ("乙",  36.0,   72.0),
    ("丙",  72.0,  108.0),
    ("丁", 108.0,  144.0),
    ("戊", 144.0,  180.0),

    ("己", 180.0,  216.0),
    ("庚", 216.0,  252.0),
    ("辛", 252.0,  288.0),
    ("壬", 288.0,  324.0),
    ("癸", 324.0,  360.0),

]


def create_stem_layer():
    """
    Layer10 : 十天干
    """

    layer = []

    for index, (name, start, end) in enumerate(heavenly_stems, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                stem=name

            )

        )

    return layer

# ==========================================================
# Layer11 : 十二支
# ==========================================================

earthly_branches = [

    ("子",   0.0,   30.0),
    ("丑",  30.0,   60.0),
    ("寅",  60.0,   90.0),
    ("卯",  90.0,  120.0),
    ("辰", 120.0,  150.0),
    ("巳", 150.0,  180.0),

    ("午", 180.0,  210.0),
    ("未", 210.0,  240.0),
    ("申", 240.0,  270.0),
    ("酉", 270.0,  300.0),
    ("戌", 300.0,  330.0),
    ("亥", 330.0,  360.0),

]


def create_branch_layer():
    """
    Layer11 : 十二支
    """

    layer = []

    for index, (name, start, end) in enumerate(earthly_branches, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                branch=name

            )

        )

    return layer

# ==========================================================
# Layer12 : 九星
# ==========================================================

nine_stars = [

    ("一白水星",   0.0,   40.0),
    ("二黒土星",  40.0,   80.0),
    ("三碧木星",  80.0,  120.0),
    ("四緑木星", 120.0,  160.0),
    ("五黄土星", 160.0,  200.0),
    ("六白金星", 200.0,  240.0),
    ("七赤金星", 240.0,  280.0),
    ("八白土星", 280.0,  320.0),
    ("九紫火星", 320.0,  360.0),

]


def create_nine_star_layer():
    """
    Layer12 : 九星
    """

    layer = []

    for index, (name, start, end) in enumerate(nine_stars, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                nine_star=name

            )

        )

    return layer

# ==========================================================
# Layer13 : 360度目盛
# ==========================================================

degree360 = []

for degree in range(360):

    degree360.append(

        (
            f"{degree}°",
            float(degree),
            float(degree + 1),
        )

    )


def create_degree_layer():
    """
    Layer13 : 360度目盛
    """

    layer = []

    for index, (name, start, end) in enumerate(degree360, start=1):

        layer.append(

            create_angle_record(

                index=index,

                start=start,

                end=end,

                degree=name

            )

        )

    return layer

# ==========================================================
# Master生成
# ==========================================================

def build_master():

    return {

        "Layer01": create_center_layer(),

        "Layer02": create_bagua_layer(),

        "Layer03": create_ground24_layer(),

        "Layer04": create_heaven24_layer(),

        "Layer05": create_human24_layer(),

        "Layer06": create_dragon60_layer(),

        "Layer07": create_gold120_layer(),

        "Layer08": create_host_layer(),

        "Layer09": create_solar_term_layer(),

        "Layer10": create_stem_layer(),

        "Layer11": create_branch_layer(),

        "Layer12": create_nine_star_layer(),

        "Layer13": create_degree_layer(),

    }

# ==========================================================
# JSON出力
# ==========================================================

if __name__ == "__main__":

    master = build_master()

    with open(

        "master.json",

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            master,

            f,

            ensure_ascii=False,

            indent=2

        )

    print("master.json generated.")

