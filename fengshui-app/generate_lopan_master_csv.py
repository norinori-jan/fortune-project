# generate_lopan_master_csv.py
# 24層（逆行二十四節気）、23層（二十八宿）、1〜4層（干支・九星・卦運・爻象）を統合し、CSV出力するスクリプト

import csv
import math

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

hosts = [
    (323.0, 343.0, "危"),
    (343.0, 353.0, "虚"),
    (353.0, 360.0, "女"),
    (0.0, 12.0, "牛"),
    (12.0, 36.0, "斗"),
    (36.0, 45.0, "箕"),
    (45.0, 60.0, "尾"),
    (60.0, 68.0, "心"),
    (68.0, 73.0, "房"),
    (73.0, 91.0, "氏"),
    (91.0, 102.0, "亢"),
    (102.0, 113.0, "角"),
    (113.0, 127.0, "軫"),
    (127.0, 144.0, "翌"),
    (144.0, 161.0, "張"),
    (161.0, 169.0, "星"),
    (169.0, 186.0, "柳"),
    (186.0, 191.0, "鬼"),
    (191.0, 222.0, "井"),
    (222.0, 233.0, "参"),
    (233.0, 234.0, "觜"),
    (234.0, 249.0, "畢"),
    (249.0, 258.0, "昂"),
    (258.0, 270.0, "胃"),
    (270.0, 283.0, "婁"),
    (283.0, 294.0, "奎"),
    (294.0, 309.0, "壁"),
    (309.0, 323.0, "室"),
]

terms = [
    (300.0, 315.0, "春分"),
    (285.0, 300.0, "清明"),
    (270.0, 285.0, "穀雨"),
    (255.0, 270.0, "立夏"),
    (240.0, 255.0, "小満"),
    (225.0, 240.0, "芒種"),
    (210.0, 225.0, "夏至"),
    (195.0, 210.0, "小暑"),
    (180.0, 195.0, "大暑"),
    (165.0, 180.0, "立秋"),
    (150.0, 165.0, "処暑"),
    (135.0, 150.0, "白露"),
    (120.0, 135.0, "秋分"),
    (105.0, 120.0, "寒露"),
    (90.0, 105.0, "霜降"),
    (75.0, 90.0, "立冬"),
    (60.0, 75.0, "小雪"),
    (45.0, 60.0, "大雪"),
    (30.0, 45.0, "冬至"),
    (15.0, 30.0, "小寒"),
    (0.0, 15.0, "大寒"),
    (345.0, 360.0, "立春"),
    (330.0, 345.0, "雨水"),
    (315.0, 330.0, "啓蟄"),
]

sector = 360.0 / 64.0
anchor_index = 13
anchor_start = 15.0
base_start = anchor_start - anchor_index * sector


def normalize(angle):
    if abs(angle - 360.0) < 1e-9:
        return 360.0
    value = angle % 360.0
    return 360.0 if abs(value - 360.0) < 1e-9 else value


def find_term(angle):
    a = normalize(angle)
    for lo, hi, name in terms:
        if lo <= a < hi or (hi == 360.0 and a == 360.0):
            return name
    return "不明"


def find_host(angle):
    a = normalize(angle)
    for lo, hi, name in hosts:
        if lo <= a < hi or (hi == 360.0 and a == 360.0):
            return name
    return "不明"


def find_entry(angle):
    a = normalize(angle)
    idx = int(math.floor((a - base_start) / sector))
    if idx < 0:
        idx += 64
    idx %= 64
    return entries[idx]


def get_boundaries():
    boundaries = set()
    boundaries.add(0.0)
    boundaries.add(360.0)
    boundaries.update([i * 15.0 for i in range(25)])
    boundaries.update([lo for lo, _, _ in hosts])
    boundaries.update([hi for _, hi, _ in hosts])
    boundaries.update([normalize(base_start + i * sector) for i in range(65)])
    return sorted(boundaries)


def split_segments():
    boundaries = get_boundaries()
    segments = []
    for i in range(len(boundaries) - 1):
        start = boundaries[i]
        end = boundaries[i + 1]
        if end - start < 1e-9:
            continue
        segments.append((start, end))
    return segments


def get_segments():
    raw = []
    boundaries = get_boundaries()
    for start, end in split_segments():
        mid = (start + end) / 2.0
        term = find_term(mid)
        host = find_host(mid)
        ganchu, kyusei, unsu, kokei = find_entry(mid)
        raw.append((start, end, term, ganchu, kyusei, unsu, kokei, host))
    return raw


def format_angle(angle):
    return f"{angle:.3f}"


def main():
    rows = get_segments()
    # 回転開始を300度に揃え、300度から360度、0度から300度の順にする
    rows = sorted(rows, key=lambda x: normalize(x[0]) if x[0] >= 300.0 or x[0] < 300.0 else x[0])
    # rotate to start at 300.0
    start_index = next((i for i, r in enumerate(rows) if abs(normalize(r[0]) - 300.0) < 1e-9), None)
    if start_index is None:
        start_index = 0
    rows = rows[start_index:] + rows[:start_index]

    with open('lopan_master_v1.csv', 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow([
            'index',
            'start_angle',
            'end_angle',
            'solar_term',
            'ganchu',
            'kyusei',
            'unsu',
            'kokei',
            'niju_hasshuku',
        ])
        for i, (start, end, term, ganchu, kyusei, unsu, kokei, host) in enumerate(rows, start=1):
            writer.writerow([
                i,
                format_angle(normalize(start)),
                format_angle(normalize(end)),
                term,
                ganchu,
                kyusei,
                unsu,
                kokei,
                host,
            ])

    print(f"Generated lopan_master_v1.csv with {len(rows)} rows.")


if __name__ == '__main__':
    main()
