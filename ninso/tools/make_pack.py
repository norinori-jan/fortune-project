"""観相の全文（非公開）を、iPhone に取り込める1つのファイル（ninso-pack.json）にまとめる。

使い方: python ninso/tools/make_pack.py [出力先.json]
出力ファイルには全文が入る。リポジトリには入れず、自分の iPhone にだけ渡すこと。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "fortune-core"))
from fortune_core import ninso_library as n  # noqa: E402


def build() -> dict:
    vols = []
    for v in n.load_volumes():
        vols.append({"no": v["no"], "title": v["title"],
                     "sections": [{"title": s["title"], "text": s["text"],
                                   "printed_page": s["printed_page"], "seq": s["seq"]} for s in v["sections"]]})
    return {"version": 1, "variants": [n._VAR_FROM, n._VAR_TO], "face_types": n.face_types(), "volumes": vols}


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else "ninso-pack.json")
    pack = build()
    out.write_text(json.dumps(pack, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    pages = sum(len(v["sections"]) for v in pack["volumes"])
    print(f"{len(pack['volumes'])}巻 {pages}ページ → {out}（{out.stat().st_size/1e6:.1f} MB）")
