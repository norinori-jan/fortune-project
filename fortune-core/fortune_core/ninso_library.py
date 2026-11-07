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
_VARIANTS = str.maketrans(
    "觀體氣會學國點變眞實圖對發數髮顏兩當禮號傳價寶靈戀舊缺絲縣假劍惡藝勞榮營驗險處営貳殘歲絕總縱續讀鐵鹽齒龜濱邊澤藏嶋",
    "観体気会学国点変真実図対発数髪顔両当礼号伝価宝霊恋旧欠糸県仮剣悪芸労栄栄験険処栄弐残歳絶総縦続読鉄塩歯亀浜辺沢蔵島",
)


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
