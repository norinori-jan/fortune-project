"""観相（人相）の書き起こしライブラリ。巻ごとの JSON（ninso/data/private/dai01.json, dai02.json …）を読む。

- 全文は公開リポジトリに置かない（.gitignore）。ファイルが無い環境（Render など）では、空として動く。
- 型・部位の名前（ninso/data/public/face_types.json）から、全巻の節を探して、巻とページ付きで返す。
- 巻ごとの記述は混ぜず、巻の番号つきで返す（巻によって言い方が変わるため）。
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[2]


def private_dir() -> Path:
    return Path(os.environ.get("NINSO_PRIVATE_DIR") or _ROOT / "ninso" / "data" / "private")


def public_dir() -> Path:
    return _ROOT / "ninso" / "data" / "public"


def _vol_no(p: Path) -> int:
    m = re.search(r"(\d+)", p.stem)
    return int(m.group(1)) if m else 0


def load_volumes() -> list[dict]:
    d = private_dir()
    out = []
    if not d.is_dir():
        return out
    for p in sorted(d.glob("dai*.json"), key=_vol_no):
        try:
            doc = json.loads(p.read_text(encoding="utf-8-sig"))
        except (OSError, ValueError):
            continue
        pages = {pg["seq"]: pg for pg in doc.get("pages", [])}
        secs = []
        for s in doc.get("sections", []):
            pg = pages.get(s.get("start_seq"), {})
            secs.append({"title": re.sub(r"\s+", "", s.get("title", "")), "text": s.get("text", ""),
                         "printed_page": pg.get("printed_page"), "seq": s.get("start_seq")})
        out.append({"file": p.name, "no": _vol_no(p), "title": doc.get("title", p.stem), "sections": secs})
    return out


def face_types() -> dict:
    p = public_dir() / "face_types.json"
    try:
        return json.loads(p.read_text(encoding="utf-8-sig"))
    except (OSError, ValueError):
        return {}


def _ref(v: dict, s: dict) -> str:
    pg = f" p.{s['printed_page']}" if s.get("printed_page") else ""
    return f"{v['title']}{pg}"


def search(query: str, limit: int = 20) -> list[dict]:
    """節の題に query を含むものを先に、本文に含むものを後に返す。"""
    q = re.sub(r"\s+", "", query)
    if not q:
        return []
    head, body = [], []
    for v in load_volumes():
        for s in v["sections"]:
            item = {"volume": v["no"], "ref": _ref(v, s), "title": s["title"], "text": s["text"]}
            if q in s["title"]:
                head.append(item)
            elif q in s["text"]:
                body.append(item)
    return (head + body)[:limit]


def lookup_type(key: str) -> dict:
    """型・質のキー（yu, kinkotsu など）から、名前と、全巻の該当節を返す。"""
    ft = face_types()
    name = None
    for grp in ft.values():
        if isinstance(grp, list):
            for e in grp:
                if e.get("key") == key:
                    name = e.get("name")
    if not name:
        return {"key": key, "name": None, "sections": []}
    secs = [s for s in search(name) if name in s["title"] or True]
    return {"key": key, "name": name, "sections": secs}
