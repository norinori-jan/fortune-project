"""易の辞書（真勢易秘訣・要約）の API。使い方は2通りで、混ぜない。

  1. 辞書引き   GET  /fortune/eki/dict, /fortune/eki/dict/{番号}   （占わない）
  2. 易の解釈   POST /fortune/eki/reading                         （出た卦＋相談 → 該当する占断）
"""
from __future__ import annotations

from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from fortune_core.iching import eki_dict

router = APIRouter(prefix="/fortune/eki", tags=["fortune-eki"])


class EkiReadingRequest(BaseModel):
    number: int
    changed_number: Optional[int] = None
    changing_lines: List[int] = []
    question: str = ""
    question_type: Optional[str] = None


@router.get("/dict")
def dict_lookup(
    number: Optional[int] = None,
    question: Optional[str] = None,
    field: Optional[str] = None,
    word: Optional[str] = None,
    limit: int = 50,
) -> dict:
    return eki_dict.lookup_dict(
        number=number, question=question, field=field, word=word,
        limit=min(max(limit, 1), 200),
    )


@router.get("/dict/{number}")
def dict_hexagram(number: int, question: Optional[str] = None) -> dict:
    entry = eki_dict.hexagram_entry(number, question)
    if entry is None:
        raise HTTPException(404, "卦が見つかりません")
    return entry


@router.post("/reading")
def reading(req: EkiReadingRequest) -> dict:
    if not 1 <= req.number <= 64:
        raise HTTPException(400, "卦番号は1〜64です")
    return eki_dict.eki_reading(
        number=req.number,
        changed_number=req.changed_number,
        changing_lines=req.changing_lines,
        question_text=req.question,
        question_type=req.question_type,
    )
