"""層ごとのデータの状態を表にして出す（Raw は変えない）。
実行：  python apps/lopan/engine/tools/layer_report.py   →  apps/lopan/docs/LAYER_DATA_STATUS.md
"""
import pathlib, sys, collections
HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import lopan_service as S

OUT = HERE.parents[1] / "docs" / "LAYER_DATA_STATUS.md"
NOTE = {
    14: "最初の区分と63番目にだけ角度がある。残りは角度が未記入。",
    15: "64卦の並びのみ。角度は1つも無い。",
    16: "並びのみ。角度は1つも無い。",
    17: "並びのみ。角度は1つも無い。",
    18: "並びのみ（層17のファイルの中にある）。角度は無い。",
    19: "最初の区分にだけ角度（331.875°〜337.5°）。残りは未記入。",
    20: "最初の区分にだけ角度。残りは未記入。",
    21: "最初の区分にだけ角度。残りは未記入。",
    22: "記録が1件だけで、中身（左・中・右）も空。Raw の書式の確認が必要。",
    23: "25区分すべてに角度あり。区分の間に隙間があり、その角度では NO_MATCH になる。",
    25: "62区分。48番は角度が逆向きに入力されている（要確認・照合から外している）。9番は 360° をまたぐ。3番の前に隙間がある。",
    26: "記号が402件で、一周360件を超える。超えた分の扱いを決める必要がある。",
    27: "記号が368件で、一周360件を超える。329.5°起点・1°刻みで並べているため、超えた8件は起点付近と重なる。",
}


def main():
    db = S.adapted_database()
    rows = ["| 層 | 記録数 | 角度が入っている | 状態 | 備考 |", "|---|---|---|---|---|"]
    for n in range(10, 28):
        if n not in db:
            rows.append(f"| {n} | 0 | - | 未読込 | Raw ファイルがない／読めない |"); continue
        have, total = S.coverage(n)
        st = "引ける" if have == total and total else ("一部だけ" if have else "角度なし")
        rows.append(f"| {n} | {total} | {have} | {st} | {NOTE.get(n, '')} |")
    review = "\n".join(f"- 層{x['layer']} の {x['id']}番：{x['reason']}（入力は {x['angle_start']}° → {x['angle_end']}°）" for x in S.REVIEW) or "（なし）"
    txt = f"""# 層ごとのデータの状態（自動生成）

`lopan_service.py` で Raw を読み込んだ結果。**引けない層の多くは、エンジンの不具合ではなく、Raw にまだ角度が入っていないため。**
角度の補完は、Raw の約束（一般知識で補完しない）により、していない。

{chr(10).join(rows)}

## 照合から外した記録（人の確認が要る）
{review}

## 次にやること（データ側）
- 層14・19・20・21：角度が未記入の区分を、実物の羅盤から入力する。
- 層15〜18：角度を決める基準（どの層と同じ区分か）を決める。
- 層22：Raw の書式を確認する。
- 層26・27：一周を超えた記号の扱いを決める。
- 層01〜10：作り直し中（完成してから入れ直す）。

再生成：`python apps/lopan/engine/tools/layer_report.py`
"""
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(txt, encoding="utf-8")
    print(txt)


if __name__ == "__main__":
    main()
