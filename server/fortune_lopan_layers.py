"""羅盤：Raw（層10〜27）を、角度で引く。層ごとの記載をそのまま返す（意味付け・吉凶判定はしない）。

層の名称や「各層で出すもの」は、Nori が docs/LOPAN_LAYER_CATALOG.md に記入したものを正とする。
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

from fastapi import APIRouter, HTTPException, Query

_ENGINE = Path(__file__).resolve().parent.parent / "apps" / "lopan" / "engine"
if str(_ENGINE) not in sys.path:
    sys.path.insert(0, str(_ENGINE))

import lopan_service as _svc  # noqa: E402

router = APIRouter(prefix="/fortune/lopan", tags=["fortune-lopan-layers"])


@router.get("/layers")
def layers() -> dict[str, Any]:
    out = []
    for n in sorted(k for k in _svc.adapted_database() if isinstance(k, int)):
        with_angle, total = _svc.coverage(n)
        out.append({"layer": n, "total": total, "with_angle": with_angle})
    return {"layers": out, "note": "層の名称・意味は付けていない（Raw の約束）。"}


@router.get("/measure")
def measure(angle: float = Query(..., ge=0, le=360)) -> dict[str, Any]:
    try:
        return _svc.measure(angle)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(500, f"羅盤の読み込みに失敗しました：{exc}") from exc
