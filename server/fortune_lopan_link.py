"""羅盤 × 四柱推命：四柱の結果（五行）と九星から、吉方位を出す。

元データは core/registry_a.json（lopan.later_heaven_bagua / lopan.lucky_directions_by_kyusei）。
本格的な方位学（年盤・月盤・日盤の九星の飛びを見る）ではなく、本命星に対する登録済みの吉方位と、
命式で不足している五行を補う方位（後天定位盤の五行）を合わせて示す。AI は使わない。
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

_ROOT = Path(__file__).resolve().parent.parent
_core = str(_ROOT / "fortune-core")
if _core not in sys.path:
    sys.path.insert(0, _core)

from fortune_core.shichu_simple import four_pillars  # noqa: E402

router = APIRouter(prefix="/fortune/lopan", tags=["fortune-lopan-link"])

STEM_EL = dict(zip("甲乙丙丁戊己庚辛壬癸", ["wood", "wood", "fire", "fire", "earth", "earth", "metal", "metal", "water", "water"]))
BRANCH_EL = dict(zip("子丑寅卯辰巳午未申酉戌亥", ["water", "earth", "wood", "wood", "earth", "fire", "fire", "earth", "metal", "metal", "earth", "water"]))
EL_JA = {"wood": "木", "fire": "火", "earth": "土", "metal": "金", "water": "水"}
DIR_JA = {"N": "北", "NE": "北東", "E": "東", "SE": "南東", "S": "南", "SW": "南西", "W": "西", "NW": "北西"}
STARS = {1: "一白水星", 2: "二黒土星", 3: "三碧木星", 4: "四緑木星", 5: "五黄土星", 6: "六白金星", 7: "七赤金星", 8: "八白土星", 9: "九紫火星"}

_registry: dict[str, Any] | None = None


def _lopan() -> dict[str, Any]:
    global _registry
    if _registry is None:
        _registry = json.loads((_ROOT / "core" / "registry_a.json").read_text(encoding="utf-8"))["lopan"]
    return _registry


def honmei_star(year: int) -> int:
    """本命星（立春で切り替えた年から）。例：2024→三碧、2026→一白。"""
    m = year % 9 or 9
    n = 11 - m
    return n - 9 if n > 9 else n


class LinkRequest(BaseModel):
    birth_date: str = Field(..., description="YYYY-MM-DD")
    birth_time: str | None = Field(None, description="HH:MM（分からなければ省略）")


@router.post("/link")
def lopan_link(req: LinkRequest) -> dict[str, Any]:
    try:
        d = datetime.strptime(req.birth_date, "%Y-%m-%d")
        t = datetime.strptime(req.birth_time, "%H:%M") if req.birth_time else None
    except ValueError as exc:
        raise HTTPException(400, "birth_date は YYYY-MM-DD、birth_time は HH:MM で入れてください") from exc
    dt = d.replace(hour=t.hour, minute=t.minute) if t else d.replace(hour=12)
    pil = four_pillars(dt, hour_known=bool(t))

    # 本命星は、立春で切り替えた「年柱の年」で決める
    year = dt.year - 1 if (dt.month <= 2 and pil["sun_longitude"] < 315.0) else dt.year
    star = honmei_star(year)

    # 命式の五行（天干と地支）を数える
    count = {k: 0 for k in EL_JA}
    for key in ("year", "month", "day", "hour"):
        if key in pil:
            count[STEM_EL[pil[key]["stem"]]] += 1
            count[BRANCH_EL[pil[key]["branch"]]] += 1
    lacking = min(count, key=lambda k: (count[k], list(EL_JA).index(k)))
    dominant = max(count, key=lambda k: (count[k], -list(EL_JA).index(k)))
    day_master = STEM_EL[pil["day"]["stem"]]

    lp = _lopan()
    lucky = lp["lucky_directions_by_kyusei"].get(str(star), {"best": [], "avoid": []})
    best = [x for x in lucky.get("best", [])]
    avoid = [x for x in lucky.get("avoid", [])]
    support = [k for k, v in lp["later_heaven_bagua"].items() if v["wuxing"] == lacking]
    # 日主を生かす（日主を生む五行）の方位も添える
    sheng = {"wood": "water", "fire": "wood", "earth": "fire", "metal": "earth", "water": "metal"}
    helper = sheng[day_master]
    helper_dirs = [k for k, v in lp["later_heaven_bagua"].items() if v["wuxing"] == helper]

    ja = lambda ds: [{"key": k, "ja": DIR_JA.get(k, k)} for k in ds]  # noqa: E731
    return {
        "pillars": pil,
        "honmei": {"number": star, "name": STARS[star], "year_used": year},
        "elements": {"count": {EL_JA[k]: v for k, v in count.items()}, "dominant": EL_JA[dominant],
                     "lacking": EL_JA[lacking], "day_master": EL_JA[day_master]},
        "directions": {
            "best": ja(best),
            "avoid": ja([] if avoid == ["all"] else avoid),
            "avoid_all": avoid == ["all"],
            "support_lacking": ja(support),
            "support_day_master": ja(helper_dirs),
        },
        "summary": (
            f"本命星は{STARS[star]}。吉方位は{('・'.join(DIR_JA[k] for k in best)) or 'なし'}"
            f"（避ける方位：{'すべて' if avoid == ['all'] else ('・'.join(DIR_JA[k] for k in avoid) or 'なし')}）。"
            f"命式では{EL_JA[lacking]}が不足しているので、{('・'.join(DIR_JA[k] for k in support)) or '該当なし'}の方位が補いになります。"
        ),
        "note": "目安です。年盤・月盤・日盤の九星の飛びまでは見ていません（登録済みの本命星の吉方位と、命式の五行から出しています）。",
    }
