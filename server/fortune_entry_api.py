"""入口の API：相談内容から、最適な占術を選び（/fortune/entry）、タロットのケルト十字を引く（/fortune/tarot/celtic）。

単体の fortune-core にあった「占いの入り口」（DivineEntryEngine）と、78枚のタロットエンジン（TarotEngine）を、
hub の API から使えるようにしたもの。追加のみ（既存の API は変えない）。
"""
from __future__ import annotations

import sys
import time
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

_CORE = Path(__file__).resolve().parent.parent / "fortune-core"
if str(_CORE) not in sys.path:
    sys.path.append(str(_CORE))

from fortune_core.divination_entry import DivineEntryEngine  # noqa: E402
from fortune_core.tarot_engine import TarotEngine  # noqa: E402

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


@router.post("/entry")
def entry(req: EntryRequest) -> dict[str, Any]:
    """相談内容を分類し、おすすめの占術と案内文を返す。"""
    return _entry.create_entry(req.question).to_dict()


@router.post("/tarot/celtic")
def tarot_celtic(req: CelticRequest) -> dict[str, Any]:
    """ケルト十字（10枚）を引く。"""
    seed = req.seed if req.seed is not None else int(time.time() * 1000)
    try:
        return _tarot_engine().draw_celtic_cross(seed, req.question)
    except FileNotFoundError as e:
        raise HTTPException(status_code=500, detail=str(e))
