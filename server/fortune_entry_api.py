"""入口の API：相談内容から、最適な占術を選び（/fortune/entry）、タロットのケルト十字を引き（/fortune/tarot/celtic）、四柱を求める（/fortune/shichu/pillars）。

単体の fortune-core にあった「占いの入り口」（DivineEntryEngine）と、78枚のタロットエンジン（TarotEngine）を、
hub の API から使えるようにしたもの。追加のみ（既存の API は変えない）。
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from datetime import datetime
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

_CORE = Path(__file__).resolve().parent.parent / "fortune-core"
if str(_CORE) not in sys.path:
    sys.path.append(str(_CORE))

from fortune_core.divination_entry import DivineEntryEngine  # noqa: E402
from fortune_core.tarot_engine import TarotEngine  # noqa: E402
from fortune_core.shichu_simple import four_pillars  # noqa: E402
from fortune_core.shichu_meishiki import build_meishiki  # noqa: E402
from fortune_core.entry_router import route  # noqa: E402

router = APIRouter(prefix="/fortune", tags=["fortune-entry"])
_entry = DivineEntryEngine()
_tarot: TarotEngine | None = None


def _tarot_engine() -> TarotEngine:
    global _tarot
    if _tarot is None:
        _tarot = TarotEngine()
    return _tarot


class EntryRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=500)


class CelticRequest(BaseModel):
    question: str = Field(default="", max_length=500)
    seed: int | None = Field(default=None, description="省略すると現在時刻（ミリ秒）")


class PillarsRequest(BaseModel):
    birth_date: str = Field(..., description="YYYY-MM-DD")
    birth_time: str | None = Field(default=None, description="HH:MM（日本時間。分からなければ省略）")


class MeishikiRequest(PillarsRequest):
    gender: str = Field(default="男", description="男 または 女")


@router.post("/shichu/meishiki")
def shichu_meishiki(req: MeishikiRequest) -> dict[str, Any]:
    """命式（通変星・蔵干・十二運・五行点数・格局・用神・大運・日干鑑定）。AI を使わない。"""
    if req.gender not in ("男", "女"):
        raise HTTPException(status_code=422, detail="gender は 男 か 女")
    try:
        d = datetime.strptime(req.birth_date, "%Y-%m-%d")
        known = bool(req.birth_time)
        if known:
            t = datetime.strptime(req.birth_time, "%H:%M")
            d = d.replace(hour=t.hour, minute=t.minute)
    except ValueError:
        raise HTTPException(status_code=422, detail="日付は YYYY-MM-DD、時刻は HH:MM で入力してください")
    return build_meishiki(d, req.gender, known)


@router.post("/shichu/pillars")
def shichu_pillars(req: PillarsRequest) -> dict[str, Any]:
    """生年月日（と時刻）から四柱を求める（簡易計算）。"""
    try:
        d = datetime.strptime(req.birth_date, "%Y-%m-%d")
        if req.birth_time:
            t = datetime.strptime(req.birth_time, "%H:%M")
            d = d.replace(hour=t.hour, minute=t.minute)
    except ValueError:
        raise HTTPException(status_code=400, detail="日付は YYYY-MM-DD、時刻は HH:MM で入れてください")
    return four_pillars(d, hour_known=bool(req.birth_time))


@router.post("/entry")
def entry(req: EntryRequest) -> dict[str, Any]:
    """相談内容を分類し、おすすめの占術（recommended）と、相談の種類（concern_type）を返す。"""
    d = _entry.create_entry(req.question).to_dict()
    return {"question": req.question, "concern_type": d.get("concern_type"), "recommended": route(req.question), "engine": d}


@router.post("/tarot/celtic")
def tarot_celtic(req: CelticRequest) -> dict[str, Any]:
    """ケルト十字（10枚）を引く。"""
    seed = req.seed if req.seed is not None else int(time.time() * 1000)
    try:
        res = _tarot_engine().draw_celtic_cross(seed, req.question)
        from fortune_core.tarot_reading import build_reading
        res["reading"] = build_reading(res["positions"], req.question)
        return res
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
