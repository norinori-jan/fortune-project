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


# 旧字体・異体字 → 新字体（照合のためだけ。返す本文は書き起こしのまま）
_VAR_FROM = "觀體氣會學國點變眞實圖對發數髮顏兩當禮號傳價寶靈戀舊缺絲縣假劍惡藝勞榮營驗險處営貳殘歲絕總縱續讀鐵鹽齒龜濱邊澤藏嶋"
_VAR_TO = "観体気会学国点変真実図対発数髪顔両当礼号伝価宝霊恋旧欠糸県仮剣悪芸労栄栄験険処栄弐残歳絶総縦続読鉄塩歯亀浜辺沢蔵島"
_VARIANTS = str.maketrans(_VAR_FROM, _VAR_TO)


def norm(text: str) -> str:
    """空白を除き、旧字体・異体字を新字体にそろえる（照合用）。"""
    return re.sub(r"\s+", "", text or "").translate(_VARIANTS)


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


def _excerpt(text: str, q: str, width: int = 40) -> str:
    """本文のうち最初に q が出る前後だけを短く返す（空白・改行は詰める）。"""
    t = "".join(text.split())
    nt = norm(t)
    i = nt.find(q)
    if i < 0:
        return t[: width * 2]
    lo, hi = max(0, i - width), min(len(t), i + len(q) + width)
    return ("…" if lo else "") + t[lo:hi] + ("…" if hi < len(t) else "")


def search(query: str, limit: int = 20) -> list[dict]:
    """節の題に含むものを先に、残りは本文での出現回数の多い順。count と excerpt を付ける。"""
    q = norm(query)
    if not q:
        return []
    head, body = [], []
    for v in load_volumes():
        for s in v["sections"]:
            nt, nb = norm(s["title"]), norm(s["text"])
            c = nb.count(q) + nt.count(q)
            if not c:
                continue
            item = {"volume": v["no"], "ref": _ref(v, s), "title": s["title"],
                    "text": s["text"], "count": c, "excerpt": _excerpt(s["text"], q)}
            (head if q in nt else body).append(item)
    head.sort(key=lambda x: -x["count"])
    body.sort(key=lambda x: -x["count"])
    return (head + body)[:limit]


# ---- いろいろな観点からの検索（部位・話題・型・質・言葉・巻） ----
_MARK_L, _MARK_R = "⟦", "⟧"
_cache: dict = {"sig": None, "vols": []}


def _indexed() -> list[dict]:
    """巻を読み、各節に照合用の本文(_n)を付けて覚えておく（ファイルが変わったら読み直す）。"""
    d = private_dir()
    sig = tuple((p.name, p.stat().st_mtime_ns) for p in sorted(d.glob("dai*.json"))) if d.is_dir() else ()
    if _cache["sig"] != (str(d), sig):
        vols = load_volumes()
        for v in vols:
            for sec in v["sections"]:
                sec["_n"] = norm(sec["title"] + "\n" + sec["text"])
                sec["_flat"] = "".join(sec["text"].split())
        _cache["sig"], _cache["vols"] = (str(d), sig), vols
    return _cache["vols"]


def _group_of(key: str) -> dict | None:
    """キー（me, zaiun, yu …）→ {key, name, kind, terms}。terms は「いずれか」の言い方。"""
    for kind, grp in face_types().items():
        if not isinstance(grp, list):
            continue
        for e in grp:
            if e.get("key") == key:
                terms = [e["name"]] + list(e.get("aliases", [])) + list(e.get("terms", []))
                return {"key": key, "name": e["name"], "kind": kind, "terms": list(dict.fromkeys(terms))}
    return None


def facets() -> dict:
    """画面の選択肢：部位・話題・型・質、読み込めた巻、各キーが出るページ数。"""
    ft = face_types()
    vols = _indexed()
    out: dict = {"volumes": [{"no": v["no"], "title": v["title"], "pages": len(v["sections"])} for v in vols],
                 "groups": []}
    labels = {"face_parts": "部位", "topics": "話題", "face_shapes": "顔の型（十字面法）", "three_qualities": "三つの質"}
    for kind in ("face_parts", "topics", "face_shapes", "three_qualities"):
        items = []
        for e in ft.get(kind, []):
            g = _group_of(e["key"])
            terms = [norm(t) for t in g["terms"]]
            n = sum(1 for v in vols for sec in v["sections"] if any(t in sec["_n"] for t in terms))
            items.append({"key": e["key"], "name": e["name"], "pages": n})
        out["groups"].append({"kind": kind, "label": labels[kind], "items": items})
    return out


def _mark(flat: str, terms: list[str], lo: int, hi: int) -> str:
    seg = flat[lo:hi]
    nseg = norm(seg)
    spans = []
    for t in terms:
        i = 0
        while t and (i := nseg.find(t, i)) >= 0:
            spans.append((i, i + len(t)))
            i += len(t)
    spans.sort()
    out, last = [], 0
    for a, b in spans:
        if a < last:
            continue
        out += [seg[last:a], _MARK_L, seg[a:b], _MARK_R]
        last = b
    out.append(seg[last:])
    return "".join(out)


def find(keys: list[str] | None = None, q: str = "", volume: int | None = None, mode: str = "all",
         limit: int = 20, offset: int = 0) -> dict:
    """キー（部位・話題・型・質）と自由な言葉を組み合わせて探す。

    mode="all": 選んだものがすべて同じページに出るページ。mode="any": どれか一つでも出るページ。
    自由な言葉は空白で区切ると、それぞれが一つの条件。結果は該当の濃い順。by_volume は巻ごとの該当ページ数。
    """
    groups = []
    for k in keys or []:
        g = _group_of(k)
        if g:
            groups.append({"label": g["name"], "terms": [norm(t) for t in g["terms"]], "raw": g["terms"]})
    for w in (q or "").split():
        nw = norm(w)
        if nw:
            groups.append({"label": w, "terms": [nw], "raw": [w]})
    if not groups:
        return {"total": 0, "results": [], "by_volume": {}, "labels": []}
    want_all = mode != "any"
    hits, by_vol = [], {}
    for v in _indexed():
        for sec in v["sections"]:
            per = [sum(sec["_n"].count(t) for t in g["terms"]) for g in groups]
            ok = all(per) if want_all else any(per)
            if not ok:
                continue
            by_vol[v["no"]] = by_vol.get(v["no"], 0) + 1
            if volume and v["no"] != volume:
                continue
            hits.append((sum(per), v, sec, per))
    hits.sort(key=lambda x: (-x[0], x[1]["no"], x[2]["seq"] or 0))
    res = []
    for score, v, sec, per in hits[offset: offset + limit]:
        flat = sec["_flat"]
        nflat = norm(flat)
        alls = [t for g in groups for t in g["terms"]]
        first = [nflat.find(t) for t in alls if t in nflat]
        c = min(first) if first else 0
        lo, hi = max(0, c - 45), min(len(flat), c + 95)
        res.append({"volume": v["no"], "seq": sec["seq"], "ref": _ref(v, sec), "title": sec["title"],
                    "count": score,
                    "matched": [g["label"] for g, n in zip(groups, per) if n],
                    "excerpt": ("…" if lo else "") + _mark(flat, alls, lo, hi) + ("…" if hi < len(flat) else "")})
    return {"total": len(hits), "results": res, "by_volume": by_vol, "labels": [g["label"] for g in groups],
            "terms": [t for g in groups for t in g["raw"]]}


def page(volume: int, seq: int) -> dict | None:
    """1ページ分の全文と、前後のページ番号。"""
    for v in _indexed():
        if v["no"] != volume:
            continue
        secs = v["sections"]
        for i, sec in enumerate(secs):
            if sec["seq"] == seq:
                return {"volume": volume, "seq": seq, "ref": _ref(v, sec), "text": sec["text"],
                        "prev": secs[i - 1]["seq"] if i else None,
                        "next": secs[i + 1]["seq"] if i + 1 < len(secs) else None}
    return None


def lookup_type(key: str, limit: int = 20) -> dict:
    """型・質・部位のキー（yu, kinkotsu, me など）から名前と該当節を返す。別名（目↔眼）も探す。"""
    ft = face_types()
    name, aliases = None, []
    for grp in ft.values():
        if isinstance(grp, list):
            for e in grp:
                if e.get("key") == key:
                    name, aliases = e.get("name"), list(e.get("aliases", []))
    if not name:
        return {"key": key, "name": None, "sections": []}
    seen, secs = set(), []
    for w in [name] + aliases:
        for r in search(w, limit):
            k = (r["volume"], r["ref"], r["title"])
            if k not in seen:
                seen.add(k)
                secs.append(r)
    secs.sort(key=lambda x: -x["count"])
    return {"key": key, "name": name, "aliases": aliases, "sections": secs[:limit]}


def report() -> str:
    """読み込めている巻の点検（ページ数・字数・要確認ページ・型ごとの該当数）。"""
    vols = load_volumes()
    lines = [f"読み込めた巻: {len(vols)}（{private_dir()}）"]
    if not vols:
        return "\n".join(lines + ["巻がありません。dai01.json などを置いてください"])
    nos = [v["no"] for v in vols]
    miss = [n for n in range(1, max(nos) + 1) if n not in nos]
    if miss:
        lines.append(f"抜けている巻: {miss}")
    for v in vols:
        chars = sum(len(s["text"]) for s in v["sections"])
        thin = [s["seq"] for s in v["sections"] if len(s["text"]) < 30]
        lines.append(f"  第{v['no']:>2}巻  {len(v['sections']):>4}節  {chars:>7}字  文字が極端に少ないページ {len(thin)}件")
    ft = face_types()
    names = [(e["key"], e["name"]) for grp in ft.values() if isinstance(grp, list) for e in grp]
    lines.append("型・質の名前が出てくる節の数（全巻合計 / 巻ごと）:")
    for key, name in names:
        per = {v["no"]: sum(1 for s in v["sections"] if norm(name) in norm(s["text"]) or norm(name) in norm(s["title"])) for v in vols}
        hit = {n: c for n, c in per.items() if c}
        lines.append(f"  {name}({key}): {sum(per.values())}  {hit if hit else '— 見つからない'}")
    return "\n".join(lines)


if __name__ == "__main__":
    print(report())
