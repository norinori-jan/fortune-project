# 羅盤第24層（二十四節気・逆行）統合テーブル生成スクリプト
# 第1-4層: 干支/九星/卦運/爻象 (5.625度刻み)
# 第23層: 二十八宿
# 第24層: 二十四節気（逆行、春分315->300起点）

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
    (0.0, 15.0, "大寒"),
    (15.0, 30.0, "小寒"),
    (30.0, 45.0, "冬至"),
    (45.0, 60.0, "大雪"),
    (60.0, 75.0, "小雪"),
    (75.0, 90.0, "立冬"),
    (90.0, 105.0, "霜降"),
    (105.0, 120.0, "白露"),
    (120.0, 135.0, "寒露"),
    (135.0, 150.0, "秋分"),
    (150.0, 165.0, "処暑"),
    (165.0, 180.0, "立秋"),
    (180.0, 195.0, "大暑"),
    (195.0, 210.0, "小暑"),
    (210.0, 225.0, "夏至"),
    (225.0, 240.0, "芒種"),
    (240.0, 255.0, "小満"),
    (255.0, 270.0, "立夏"),
    (270.0, 285.0, "穀雨"),
    (285.0, 300.0, "清明"),
    (300.0, 315.0, "春分"),
    (315.0, 330.0, "啓蟄"),
    (330.0, 345.0, "雨水"),
    (345.0, 360.0, "立春"),
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


def normalize_for_sort(angle):
    a = angle % 360.0
    return 360.0 if abs(a - 360.0) < 1e-9 else a


def find_term(angle):
    a = normalize_for_sort(angle)
    for lo, hi, name in terms:
        if lo <= a < hi or (hi == 360.0 and a == 360.0):
            return name
    return "不明"


def find_host(angle):
    a = normalize_for_sort(angle)
    for lo, hi, name in hosts:
        if lo <= a < hi or (hi == 360.0 and a == 360.0):
            return name
    return "不明"


def find_entry(angle):
    a = normalize_for_sort(angle)
    row_index = int(math.floor((a - base_start) / sector)) if a >= base_start else int(math.floor((a + 360.0 - base_start) / sector))
    row_index %= 64
    return entries[row_index]


def split_by_boundaries(intervals, boundaries):
    boundaries = sorted(set(boundaries))
    result = []
    for start, end, meta in intervals:
        cur = start
        for b in boundaries:
            if cur < b < end - 1e-9:
                result.append((cur, b, meta))
                cur = b
        if end - cur > 1e-9:
            result.append((cur, end, meta))
    return result

# 64行の元区間を作成
raw_intervals = []
for i in range(64):
    start = base_start + i * sector
    end = start + sector
    if start < 0:
        start += 360.0
        end += 360.0
    if end < 0:
        end += 360.0
    if start >= 360.0:
        start -= 360.0
        end -= 360.0
    if end > 360.0:
        raw_intervals.append((start, 360.0, i))
        raw_intervals.append((0.0, end - 360.0, i))
    else:
        raw_intervals.append((start, end, i))

raw_intervals = sorted(raw_intervals, key=lambda x: x[0])

# 境界を設定（15度節気境界、宿境界、300開始点）
boundaries = list({i * 15.0 for i in range(25)})
for lo, hi, _ in hosts:
    boundaries.append(lo)
    boundaries.append(hi)
boundaries.extend([0.0, 300.0, 360.0])

# 区間分割
split_intervals = []
for start, end, row_idx in raw_intervals:
    relevant = [b for b in boundaries if start < b < end]
    relevant = sorted(set(relevant))
    current = start
    for b in relevant:
        split_intervals.append((current, b, row_idx))
        current = b
    split_intervals.append((current, end, row_idx))

# Table segmentsを作成
segments = []
for start, end, row_idx in split_intervals:
    if end - start < 1e-9:
        continue
    entry = entries[row_idx]
    term = find_term(start)
    host = find_host(start)
    segments.append((start, end, term, entry, host))

# 300.0スタートで順序を回転
segments = sorted(segments, key=lambda x: x[0])
idx = next((i for i, seg in enumerate(segments) if seg[0] <= 300.0 + 1e-9 < seg[1]), 0)
if idx is None:
    idx = 0
pre = segments[idx:]
post = segments[:idx]
if pre and pre[0][0] < 300.0:
    start, end, term, entry, host = pre[0]
    pre[0] = (300.0, end, term, entry, host)
    post.append((start, 300.0, term, entry, host))
segments = pre + post

print("| 行番号 | 開始角度 | 終了角度 | 第24層：節気 | 第1〜4層：干支/九星/符号/爻 | 第23層：二十八宿 |")
print("|---|---|---|---|---|---|")
for i, (start, end, term, entry, host) in enumerate(segments, start=1):
    start_disp = normalize(start)
    end_disp = normalize(end)
    if abs(start_disp - 360.0) < 1e-9:
        start_disp = 360.0
    if abs(end_disp - 360.0) < 1e-9:
        end_disp = 360.0
    row_text = f"{entry[0]}/{entry[1]}/{entry[2]}/{entry[3]}"
    print(f"| {i} | {start_disp:.3f}° | {end_disp:.3f}° | {term} | {row_text} | {host} |")

print(f"\n# 統計")
print(f"基準行14開始: {anchor_start:.3f}°")
print(f"第1-4層区分: {sector:.3f}°")
print(f"総区間数: {len(segments)}")
