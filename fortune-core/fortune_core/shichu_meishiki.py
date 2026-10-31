"""四柱推命の命式（依存ライブラリなし）。

四柱は shichu_simple.four_pillars で求め、その上に
通変星・蔵干・十二運・空亡・五行点数・格局（外格→内格）・用神/喜神・大運・日干鑑定 を載せる。
鑑定の規則と文章は、「新四柱推命」の xls（外格・内格・日干10シート）から作った
data/shichu_rules.json / data/shichu_kanshi_stems.json を使う。AI・API キーは使わない。

点数のしきい値・蔵干の日数は xls に数字がないため仮置き（rules["params"]["assumption"]）。
結果に "assumption": True を付けて返す。
"""
from __future__ import annotations

import json
from datetime import datetime, timedelta
from pathlib import Path

from .shichu_simple import BRANCHES, STEMS, four_pillars, sun_longitude

_D = Path(__file__).parent / "data"
RULES = json.loads((_D / "shichu_rules.json").read_text(encoding="utf-8"))
STEMDATA = json.loads((_D / "shichu_kanshi_stems.json").read_text(encoding="utf-8"))

EL = dict(zip(STEMS, "木木火火土土金金水水"))
GEN = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
CON = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
GROUP = {"比肩": "比劫", "劫財": "比劫", "食神": "食傷", "傷官": "食傷", "偏財": "財星", "正財": "財星",
         "偏官": "官星", "正官": "官星", "偏印": "印星", "印綬": "印星"}
UNSEI = "長生 沐浴 冠帯 建録 帝旺 衰 病 死 墓 絶 胎 養".split()
CHOSEI = {"甲": "亥", "丙": "寅", "戊": "寅", "庚": "巳", "壬": "申", "乙": "午", "丁": "酉", "己": "酉", "辛": "子", "癸": "卯"}
# 蔵干（余気, 中気, 本気）と日数（節入りからの日数で決める。一般的な配分・仮置き）
ZOUKAN = {
    "子": [("壬", 10), ("癸", 20)], "丑": [("癸", 9), ("辛", 3), ("己", 18)],
    "寅": [("戊", 7), ("丙", 7), ("甲", 16)], "卯": [("甲", 10), ("乙", 20)],
    "辰": [("乙", 9), ("癸", 3), ("戊", 18)], "巳": [("戊", 7), ("庚", 7), ("丙", 16)],
    "午": [("丙", 10), ("己", 9), ("丁", 11)], "未": [("丁", 9), ("乙", 3), ("己", 18)],
    "申": [("己", 7), ("壬", 7), ("庚", 16)], "酉": [("庚", 10), ("辛", 20)],
    "戌": [("辛", 9), ("丁", 3), ("戊", 18)], "亥": [("戊", 7), ("甲", 7), ("壬", 16)],
}
GANGO = {"甲": "己", "己": "甲", "乙": "庚", "庚": "乙", "丙": "辛", "辛": "丙", "丁": "壬", "壬": "丁", "戊": "癸", "癸": "戊"}


def tsuhen(day: str, t: str) -> str:
    a, b = EL[day], EL[t]
    same = STEMS.index(day) % 2 == STEMS.index(t) % 2
    if a == b:
        return "比肩" if same else "劫財"
    if GEN[a] == b:
        return "食神" if same else "傷官"
    if CON[a] == b:
        return "偏財" if same else "正財"
    if CON[b] == a:
        return "偏官" if same else "正官"
    return "偏印" if same else "印綬"


def unsei(day: str, b: str) -> str:
    s, i = BRANCHES.index(CHOSEI[day]), BRANCHES.index(b)
    k = (i - s) % 12 if STEMS.index(day) % 2 == 0 else (s - i) % 12
    return UNSEI[k]


def kubo(day_pillar: str) -> str:
    s, b = STEMS.index(day_pillar[0]), BRANCHES.index(day_pillar[1])
    return BRANCHES[(b - s + 10) % 12] + BRANCHES[(b - s + 11) % 12]


def _setsu_time(dt: datetime, forward: bool) -> datetime:
    """dt の直後（forward）/直前の節入り（黄経が 315+30k 度になる時刻）。二分法・誤差は数分。"""
    lon = sun_longitude(dt)
    k = int(((lon - 315.0) % 360.0) // 30)
    target = (315.0 + 30 * (k + 1 if forward else k)) % 360.0
    lo, hi = (dt, dt + timedelta(days=33)) if forward else (dt - timedelta(days=33), dt)

    def diff(t):  # 目標からの角度差（-180..180）
        return (sun_longitude(t) - target + 180) % 360 - 180

    for _ in range(40):
        mid = lo + (hi - lo) / 2
        if diff(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo + (hi - lo) / 2


def _zoukan_pick(branch: str, days_from_setsu: float):
    items = ZOUKAN[branch]
    acc = 0
    for stem, d in items:
        acc += d
        if days_from_setsu < acc:
            return stem
    return items[-1][0]


def _strength(n: float) -> str:
    p = RULES["params"]
    if n >= p["strong_at"]:
        return "強"
    if n <= p["weak_at"]:
        return "弱"
    return "中"


def _kaku(day: str, pts: dict, el_pts: dict, month_zoukan_tsuhen: str, month_stem: str, hour_stem, month_zoukan_el: str, tenkan_set: set):
    """格局を決める（外格→内格）。"""
    P = RULES["params"]
    day_yang = STEMS.index(day) % 2 == 0
    kan, zai, ins = pts["官星"], pts["財星"], pts["印星"]
    # --- 化気格（日干と、月干または時干の干合。月令が化した五行のとき）
    for partner_name, partner in (("月干", month_stem), ("時干", hour_stem)):
        if partner and GANGO[day] == partner:
            for el, d in RULES["kafuku"].items():
                if set(d["pair"]) == {day, partner} and month_zoukan_el == el:
                    return {"type": "外格", "name": f"化{el}格", "detail": f"日干{day}と{partner}{partner}が干合し、月令が{el}",
                            "kishin_el": d["kishin"], "yojin": None}
    # --- 従格（xlsの条件のとおり。強い＝しきい値以上、弱い＝しきい値以下）
    S_, W_, M_ = P["strong_at"], P["weak_at"], P["kan_many_at"]
    hi = pts["比劫"]
    cond = {
        "従旺格": hi >= S_ and kan == 0
                 and not (day_yang and kan >= M_) and not ((not day_yang) and kan >= M_ and zai >= 1),
        "従強格": hi >= S_ and kan == 0 and ins >= S_
                 and not (day_yang and kan >= M_) and not ((not day_yang) and kan >= M_ and zai >= 1),
    }
    for name, g in (("従児格", "食傷"), ("従財格", "財星"), ("従殺格", "官星")):
        ok = hi <= W_ and ins == 0 and pts[g] >= S_
        if name == "従児格" and day_yang and kan >= M_:
            ok = False
        cond[name] = ok
    for name in ("従旺格", "従児格", "従財格", "従殺格", "従強格"):
        if cond[name]:
            d = RULES["juu"][name]
            return {"type": "外格", "name": name, "detail": f"{d['group']}が強い", "kishin": d["kishin"],
                    "imu": d["imu"], "good": d["good"], "bad": d["bad"], "yojin": None}
    # --- 両神成象格（相克する二行だけ。点数が1:1〜2:3）
    live = {e: v for e, v in el_pts.items() if v > 0}
    if len(live) == 2:
        (e1, v1), (e2, v2) = sorted(live.items(), key=lambda x: x[1], reverse=True)
        if (CON[e1] == e2 or CON[e2] == e1) and v1 / v2 <= P["ryoshin_ratio"][1]:
            weak = e2
            return {"type": "外格", "name": "両神成象格", "detail": f"{e1}{v1:g}・{e2}{v2:g}（相克）",
                    "kishin_el": [weak, next(k for k, v in GEN.items() if v == weak)], "yojin": None}
    # --- 内格（月支蔵干の通変星）
    return {"type": "内格", "name": RULES["naikaku"][month_zoukan_tsuhen], "detail": f"月支蔵干が{month_zoukan_tsuhen}"}


def build_meishiki(birth: datetime, gender: str = "男", hour_known: bool = True) -> dict:
    """birth：日本時間。gender：男/女。"""
    P = RULES["params"]
    fp = four_pillars(birth, hour_known)
    pil = {k: fp[k]["name"] for k in ("year", "month", "day", "hour") if k in fp}
    day = fp["day"]["stem"]
    # 月支蔵干（節入りからの日数）
    setsu_prev = _setsu_time(birth, forward=False)
    days_from = (birth - setsu_prev).total_seconds() / 86400
    mb = fp["month"]["branch"]
    mz = _zoukan_pick(mb, days_from)
    month_t = tsuhen(day, mz)
    # 柱ごとの表
    table = {}
    for k in ("year", "month", "day", "hour"):
        if k not in fp:
            continue
        s, b = fp[k]["stem"], fp[k]["branch"]
        zk = mz if k == "month" else ZOUKAN[b][-1][0]  # 月以外は本気
        table[k] = {"kanshi": s + b, "stem": s, "branch": b,
                    "stem_tsuhen": "日主" if k == "day" else tsuhen(day, s),
                    "zoukan": zk, "zoukan_tsuhen": tsuhen(day, zk),
                    "unsei": unsei(day, b)}
    # 五行・十神グループの点数
    w = P["weights"]
    pts = {"比劫": 0.0, "食傷": 0.0, "財星": 0.0, "官星": 0.0, "印星": 0.0}
    el = {"木": 0.0, "火": 0.0, "土": 0.0, "金": 0.0, "水": 0.0}
    for k, r in table.items():
        if k != "day":
            pts[GROUP[r["stem_tsuhen"]]] += w["tenkan_other"]
            el[EL[r["stem"]]] += w["tenkan_other"]
        pts[GROUP[r["zoukan_tsuhen"]]] += w["chishi_main"]
        el[EL[r["zoukan"]]] += w["chishi_main"]
    pts[GROUP[month_t]] += w["month_branch_bonus"]
    el[EL[mz]] += w["month_branch_bonus"]
    el[EL[day]] += 1  # 日干自身
    hour_stem = table["hour"]["stem"] if "hour" in table else None
    kaku = _kaku(day, pts, el, month_t, table["month"]["stem"], hour_stem, EL[mz], {r["stem"] for r in table.values()})
    # 用神・喜神・忌神
    yj = None
    kishin = []
    if kaku["type"] == "内格":
        shown = [k for k in ("year", "month", "hour") if k in table]
        src = [table[k]["stem"] for k in shown if table[k]["stem"] == mz]
        if src:
            yj = mz + "（月支蔵干が天干に出ている）"
        elif month_t in ("偏財", "正財", "偏印", "印綬"):
            yj = mz + "（月支蔵干）"
        else:
            yj = day + "（日干）"
        ytype = GROUP[month_t] if not src else GROUP[tsuhen(day, mz)]
        # 用神の強弱
        yg = GROUP[tsuhen(day, yj[0])]
        st = _strength(pts[yg])
        if st == "強":
            kishin = RULES["tsuyosugi"][yg]
        elif st == "弱":
            kishin = RULES["yowasugi"][yg]
        kaku["yojin"] = yj
        kaku["yojin_group"] = yg
        kaku["yojin_strength"] = st
        kaku["kishin"] = kishin
    else:
        kaku.setdefault("yojin", None)
    # 大運
    yang_year = STEMS.index(fp["year"]["stem"]) % 2 == 0
    forward = (yang_year and gender == "男") or (not yang_year and gender == "女")
    t_setsu = _setsu_time(birth, forward=forward) if forward else setsu_prev
    gap_days = abs((t_setsu - birth).total_seconds()) / 86400
    start_age = round(gap_days / 3, 1)  # 3日=1年
    ms, mbr = STEMS.index(fp["month"]["stem"]), BRANCHES.index(fp["month"]["branch"])
    step = 1 if forward else -1
    daiun = []
    for i in range(1, 11):
        s, b = STEMS[(ms + step * i) % 10], BRANCHES[(mbr + step * i) % 12]
        daiun.append({"age": round(start_age + 10 * (i - 1), 1), "kanshi": s + b, "tsuhen": tsuhen(day, s), "unsei": unsei(day, b)})
    info = STEMDATA[day]
    return {
        "birth": birth.isoformat(), "gender": gender, "hour_known": hour_known,
        "pillars": pil, "table": table, "day_stem": day, "day_kubo": kubo(table["day"]["kanshi"]),
        "month_zoukan": {"stem": mz, "tsuhen": month_t, "days_from_setsu": round(days_from, 1)},
        "points": {"group": pts, "element": el},
        "kakukyoku": kaku,
        "daiun": {"direction": "順行" if forward else "逆行", "start_age": start_age, "list": daiun},
        "nikkan": {k: info[k] for k in ("head", "image", "spirit", "taboo", "text", "ability", "personality", "jobs", "organs")},
        "assumption": True,
        "note": "点数のしきい値・蔵干の日数・大運の起運（3日=1年）は仮置きです。",
    }
