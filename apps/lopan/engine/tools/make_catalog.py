"""層ごとの事実一覧（docs/LOPAN_LAYER_CATALOG.md）を、Raw から自動で作る。
意味付け・層名称は付けない。Raw の冒頭にある原文の説明を、そのまま引用する。
実行：python apps/lopan/engine/tools/make_catalog.py
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "engine"))
import lopan_service as L  # noqa: E402

RAW = ROOT / "data" / "raw"
OUT = ROOT / "docs" / "LOPAN_LAYER_CATALOG.md"


def raw_file(n):
    for name in (f"layer{n}", f"lyaer{n}"):
        p = RAW / name
        if p.exists():
            return p


def header(n, limit=22):
    p = raw_file(n)
    if not p:
        return []
    out = []
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.rstrip()
        if re.match(r"\s*raw_layer\d+\s*=", s) or s.strip().startswith(("LAYER_ID", "def ", "class ", "import ")):
            break
        if set(s.strip()) <= set("=-# \"'"):
            continue
        out.append(s)
        if len(out) >= limit:
            break
    return [x for x in out if x.strip()]


def main():
    db = L.adapted_database()
    rows, secs = [], []
    for n in sorted(k for k in db if isinstance(k, int)):
        recs = db[n]
        withang = [r for r in recs if isinstance(r, dict) and r.get("angle_start") is not None]
        keys = sorted({k for r in recs if isinstance(r, dict) for k in r if k not in ("meta", "angle_start", "angle_end")})
        rng = ""
        if withang:
            rng = f"{min(r['angle_start'] for r in withang):g}°〜{max(r['angle_end'] for r in withang):g}°"
        wa, tot = L.coverage(n)
        rows.append(f"| {n} | {tot} | {wa} | {rng} | `{', '.join(keys)}` |")
        sample = []
        for r in recs[:3]:
            t = r.get("raw_text") if isinstance(r, dict) else r
            sample.append(str(t)[:20])
        h = "\n".join("> " + x.strip() for x in header(n)) or "> （冒頭の説明なし）"
        secs.append(f"### 層{n}\n- 記録数 {tot} ／ 角度つき {wa} ／ 範囲 {rng or '—'}\n- 先頭の記載（Raw の原文）：{' ／ '.join(sample)}\n- Raw 冒頭の原文：\n{h}\n- **この層で出すもの（Nori が記入）：** \n- **他の層との関係（Nori が記入）：** \n")
    OUT.write_text(
        "# 羅盤 層カタログ（自動生成・事実のみ）\n\n"
        "Raw に記録されている事実だけを一覧にしたもの。**層の名称・意味・吉凶は付けていない**（Raw の約束）。\n"
        "「この層で出すもの」「他の層との関係」は、**Nori が記入する欄**。記入されたら、それを正として画面と API を作る。\n\n"
        "| 層 | 記録数 | 角度つき | 角度の範囲 | 持っている項目 |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n\n## 層ごとの詳細\n\n" + "\n".join(secs),
        encoding="utf-8",
    )
    print("wrote", OUT)


if __name__ == "__main__":
    main()
