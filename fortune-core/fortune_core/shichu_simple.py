"""四柱（年・月・日・時）を求める、依存ライブラリなしの簡易エンジン。

- 日柱：ユリウス日から計算（日付は日本時間の暦日。23時以降は翌日の日柱＝晩子時を翌日扱い）
- 年柱・月柱：太陽黄経（低精度式・誤差は数分程度）で節入りを判定（立春＝315°を年の切り替え、30°ごとに月）
- 時柱：五鼠遁（日干から時干を求める）。出生地による均時差・経度補正はしない（日本標準時のまま）

大運・通変星・蔵干などは含まない（壊れている既存の shichu/engine は、別途直す）。
"""
from __future__ import annotations

import math
from datetime import datetime, timedelta

STEMS = "甲乙丙丁戊己庚辛壬癸"
BRANCHES = "子丑寅卯辰巳午未申酉戌亥"


def _jdn(y: int, m: int, d: int) -> int:
    a = (14 - m) // 12
    yy = y + 4800 - a
    mm = m + 12 * a - 3
    return d + (153 * mm + 2) // 5 + 365 * yy + yy // 4 - yy // 100 + yy // 400 - 32045


def sun_longitude(dt_jst: datetime) -> float:
    """太陽の見かけの黄経（度）。dt は日本時間。"""
    ut = dt_jst - timedelta(hours=9)
    jd = _jdn(ut.year, ut.month, ut.day) - 0.5 + (ut.hour + ut.minute / 60 + ut.second / 3600) / 24
    t = (jd - 2451545.0) / 36525.0
    l0 = 280.46646 + 36000.76983 * t
    m = math.radians(357.52911 + 35999.05029 * t)
    c = (1.914602 - 0.004817 * t) * math.sin(m) + 0.019993 * math.sin(2 * m) + 0.000289 * math.sin(3 * m)
    omega = math.radians(125.04 - 1934.136 * t)
    return (l0 + c - 0.00569 - 0.00478 * math.sin(omega)) % 360.0


def _p(stem: int, branch: int) -> dict:
    return {"stem": STEMS[stem % 10], "branch": BRANCHES[branch % 12], "name": STEMS[stem % 10] + BRANCHES[branch % 12]}


def four_pillars(dt: datetime, hour_known: bool = True) -> dict:
    """dt：日本時間の生年月日時。hour_known=False のときは時柱を出さない。"""
    lon = sun_longitude(dt)
    # 年柱（立春＝黄経315°で切り替わる。1〜2月で 315° 未満なら前年）
    y = dt.year - 1 if (dt.month <= 2 and lon < 315.0) else dt.year
    ys, yb = (y - 4) % 10, (y - 4) % 12
    # 月柱（寅月＝315°〜345°）
    k = int(((lon - 315.0) % 360.0) // 30)          # 寅からの月数 0..11
    mb = (2 + k) % 12
    ms = ((ys % 5) * 2 + 2 + k) % 10
    # 日柱（23時以降は翌日）
    day = dt.date() + timedelta(days=1) if dt.hour >= 23 else dt.date()
    idx = (_jdn(day.year, day.month, day.day) + 49) % 60
    ds, db = idx % 10, idx % 12
    out = {"year": _p(ys, yb), "month": _p(ms, mb), "day": _p(ds, db), "sun_longitude": round(lon, 2),
           "note": "簡易計算（日本標準時のまま・出生地補正なし。大運・通変星は含まない）"}
    if hour_known:
        hb = ((dt.hour + 1) // 2) % 12
        hs = ((ds % 5) * 2 + hb) % 10
        out["hour"] = _p(hs, hb)
    return out
