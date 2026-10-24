"""羅盤の Raw（層10〜27）から、知識辞書・ai-hub が読める辞書パック（dict-pack v1）を作る。

実行：  python apps/lopan/engine/tools/make_dict_pack.py
出力：  apps/lopan/data/dict-pack_lopan.json

入れるのは「構造の事実」だけ（層の番号・区分数・角度の範囲・最初の記載）。
意味付け・吉凶・名称の推測は入れない（Raw の約束）。
"""
import json, pathlib, sys, time
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import lopan_service as S

OUT = HERE.parents[1] / "data" / "dict-pack_lopan.json"
NOW = int(time.time() * 1000)


def entry(id, term, kind, summary, **k):
    d = {"id": id, "term": term, "lang": "cul", "kind": kind, "summary": summary, "form": "", "parts": [], "example": "",
         "mistakes": [], "related": [], "tags": ["羅盤", "Lopan", "占い"], "sources": [{"id": "fortune-project", "title": "fortune-project / apps/lopan"}],
         "confidence": "high", "verified": False, "updatedAt": NOW}
    d.update(k); return d


def span(recs):
    st = [r.get("degree_start", r.get("angle_start")) for r in recs if isinstance(r, dict)]
    en = [r.get("degree_end", r.get("angle_end")) for r in recs if isinstance(r, dict)]
    st = [x for x in st if isinstance(x, (int, float))]; en = [x for x in en if isinstance(x, (int, float))]
    return (st[0], en[-1]) if st and en else (None, None)


def sample(recs, n=4):
    out = []
    for r in recs[:n]:
        if isinstance(r, dict):
            t = r.get("raw_text")
            out.append("・".join(map(str, t)) if isinstance(t, list) else str(t))
    return [x for x in out if x and x != "None"]


def main():
    db = S.database()
    es = []
    layer_ids = sorted(db)
    for n in layer_ids:
        recs = db[n]
        a, b = span(recs) if isinstance(recs, list) else (None, None)
        full = a is not None and abs((a - b) % 360) < 1e-6
        rng = (f"、{a}° を起点に一周" if full else f"、角度は {a}° から {b}° まで") if a is not None else ""
        sm = sample(recs)
        parts = [["区分の数", f"{len(recs)}"]]
        if a is not None:
            parts.append(["起点（最初の区分の始まり）", f"{a}°" + ("（最後の区分の終わりと同じ＝一周）" if full else f"、最後の区分の終わりは {b}°")])
        if sm:
            parts.append(["最初の記載（原文のまま）", " ／ ".join(sm)])
        es.append(entry(f"cul:羅盤-層{n}", f"羅盤 層{n}（Raw）", "concept",
                        f"羅盤の層{n}。Raw に {len(recs)} 区分が記録されている{rng}。意味付けはしていない（原文の記録のみ）。",
                        parts=parts, related=["cul:羅盤-構成", "cul:羅盤-引き方"],
                        mistakes=["層ごとに角度の書き方が違う（始まりの角度・区分の幅）。層をまたいで同じ区分と思わない。"]))
    es.append(entry("cul:羅盤-構成", "羅盤（Lopan）の構成と連携", "concept",
                    "占いの hub（fortune-project）の中で、羅盤は apps/lopan に置く。Raw（層10〜27）→ 読み込み（lopan_service）→ 角度で引く（measure）→ 画面（apps/lopan）／hub の API。知識辞書と ai-hub は、この辞書パックで同じ用語を引く。",
                    parts=[["Raw（原データ）", "apps/lopan/data/raw/layer10〜27。変更しない。"], ["読み込み・照合", "apps/lopan/engine/lopan_service.py（measure／verify）"],
                           ["画面", "apps/lopan/frontend（React）"], ["hub", "fortune-project（FastAPI・fortune-hub）"],
                           ["辞書", "この辞書パック（知識辞書・ai-hub）"], ["元のリポジトリ", "lopanproject（取り込み元。消さない）"]],
                    related=["cul:羅盤-引き方"] + [f"cul:羅盤-層{n}" for n in layer_ids]))
    es.append(entry("cul:羅盤-引き方", "羅盤 角度から各層の記載を引く（measure）", "api",
                    "角度（度）を渡すと、層10〜27の対応する記載を返す。読み取り専用で、意味付けはしない。",
                    form="measure(角度)", example="from lopan_service import measure\nmeasure(330.0)   # 層10は 辛亥（326°〜332°）",
                    parts=[["status OK", "1件だけ一致"], ["status NO_MATCH", "一致なし（未対応の層を含む）"], ["status OVERLAP", "区間が重なって複数件"], ["status NOT_REGISTERED", "その層はまだ読めていない"]],
                    mistakes=["NO_MATCH は『その角度に記載がない』とは限らない。層15〜23は照合が未対応の可能性がある。"], related=["cul:羅盤-構成"]))
    pack = {"app": "dict-pack", "version": 1, "builtAt": NOW, "entries": es}
    OUT.write_text(json.dumps(pack, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(es)} 件 → {OUT}")


if __name__ == "__main__":
    main()
