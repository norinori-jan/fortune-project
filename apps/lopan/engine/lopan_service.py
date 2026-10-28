"""羅盤サービス：Raw（層10〜27）を読み込み、角度から各層の記載を引く（読み取り専用）。

使い方：
    from lopan_service import measure
    measure(330.0)   # -> {"angle":330.0,"layers":{10:{"status":"OK","matches":[...]},...}}

方針：Raw は変更しない。意味付け・吉凶判定はしない。
"""
import importlib.util
import pathlib

HERE = pathlib.Path(__file__).resolve().parent
RAW_DIR = HERE.parent / "data" / "raw"
LAYERS = range(10, 28)


def _load(rel):
    p = HERE / rel
    spec = importlib.util.spec_from_file_location("lopan_" + p.stem, p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


_scanner = _load("integrity/angle_integrity_scanner.py")
_ar = _load("api/ar_api.py")
_ar.build_layer_adapter = _scanner.build_layer_adapter  # ar_api は adapter を取り込んでいないので、ここでつなぐ


import re

_VAR = re.compile(r"^raw_layer(\d+)\s*=\s*\[", re.M)
_CONST = re.compile(r"^([A-Za-z_][A-Za-z_0-9]*)\s*=\s*(.+)$", re.M)


def _match_bracket(text, i):
    """text[i] が '[' のとき、対応する ']' の位置を返す（文字列の中の括弧は数えない）。"""
    depth, q, k = 0, None, i
    while k < len(text):
        c = text[k]
        if q:
            if c == "\\":
                k += 1
            elif c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == "[":
            depth += 1
        elif c == "]":
            depth -= 1
            if depth == 0:
                return k
        k += 1
    return -1


def _constants(head):
    """リストより前にある、単純な定数（LAYER_ID = 10 など）を集める。"""
    ns = {}
    for m in _CONST.finditer(head):
        try:
            exec(f"{m.group(1)} = {m.group(2)}", {}, ns)
        except Exception:
            pass
    return ns


def load_database(raw_dir=RAW_DIR):
    """Raw ファイルから、{層番号: 記録のリスト} を作る。ファイルは変更しない。
    Raw ファイルは、そのままでは Python として読めない（説明文の引用符が欠け、末尾に壊れた関数が混ざる）ので、
    「raw_layerNN = [ ... ]」の部分だけを取り出して評価する。
    他の層のデータが混ざっているファイル（layer17 の中の層18 など）も拾うが、自分の名前のファイルが優先。"""
    db, own = {}, set()
    for n in LAYERS:
        p = pathlib.Path(raw_dir) / f"layer{n}"
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        for m in _VAR.finditer(text):
            layer = int(m.group(1))
            if layer not in LAYERS or (layer in db and (layer in own or layer != n)):
                continue
            j = text.index("[", m.start())
            e = _match_bracket(text, j)
            if e < 0:
                continue
            ns = _constants(text[: m.start()])
            try:
                db[layer] = eval(text[j : e + 1], {}, ns)
            except Exception:
                continue
            if layer == n:
                own.add(layer)
        if n == 27:
            recs = _layer27_records(text)
            if recs:
                db[27] = recs
    return db


_SYM = re.compile(r"^raw_layer27_symbols\s*=\s*\[", re.M)


def _layer27_records(text):
    """層27：Raw は「記号の並び」だけを持ち、角度は規則（329.5°起点・1°刻み・右回り）で付ける。
    元ファイルは関数の字下げが失われていて、そのままでは動かないので、同じ規則をここで再現する。
    記号は原文のまま。角度は計算用の値で、Raw の記号は変えない。"""
    m = _SYM.search(text)
    if not m:
        return None
    j = text.index("[", m.start())
    e = _match_bracket(text, j)
    symbols = eval(text[j : e + 1], {}, _constants(text[: m.start()]))
    cs = _constants(text[: m.start()])
    start, step = float(cs.get("ANGLE_START", 329.5)), float(cs.get("ANGLE_STEP", 1.0))
    out = []
    for i, sym in enumerate(symbols, start=1):
        a = start + (i - 1) * step
        out.append({"id": i, "angle_start": a % 360.0, "angle_end": (a + step) % 360.0, "angle_width": step, "raw_symbol": sym, "source_order": i})
    return out


_DB = None


def database():
    global _DB
    if _DB is None:
        _DB = load_database()
    return _DB


REVIEW = []   # 照合から外した記録（人の確認が要る）：[{layer, id, reason}]


def _with_angle_keys(db):
    """標準の層は degree_start / degree_end で書かれ、照合側は angle_start / angle_end を読む。
    Raw 自体は変えず、コピーに別名を足して渡す。"""
    out = {}
    for n, recs in db.items():
        if isinstance(recs, list) and recs and isinstance(recs[0], dict) and "degree_start" in recs[0] and "angle_start" not in recs[0]:
            out[n] = [dict(r, angle_start=r.get("degree_start"), angle_end=r.get("degree_end")) for r in recs]
        else:
            out[n] = recs
    # 角度が「逆向きに入力された」と記録されている区分は、勝手に直さず、照合から外して REVIEW に載せる。
    # （そのまま使うと、360°をまたぐ巨大な区間と解釈され、ほかの区分と重なって見える）
    REVIEW.clear()
    for n, recs in list(out.items()):
        if isinstance(recs, list):
            keep = []
            for r in recs:
                if isinstance(r, dict) and "reverse_angle_as_entered" in (r.get("validation_flags") or []):
                    REVIEW.append({"layer": n, "id": r.get("id"), "reason": "角度が逆向きに入力されている（要確認）",
                                   "angle_start": r.get("angle_start"), "angle_end": r.get("angle_end")})
                    r = dict(r, angle_start=None, angle_end=None)
                keep.append(r)
            out[n] = keep
    return out


_ADAPTED = None


def adapted_database():
    global _ADAPTED
    if _ADAPTED is None:
        _ADAPTED = _with_angle_keys(database())
    return _ADAPTED


def coverage(n):
    """層 n の記録のうち、角度が入っている区分の数 / 全体。"""
    recs = adapted_database().get(n) or []
    if not isinstance(recs, list):
        return 0, 0
    # 等分割で位置から引く層（24・26・27）は、角度の有無に関係なく引ける
    if n in (24, 26, 27):
        return len(recs), len(recs)
    have = sum(1 for r in recs if isinstance(r, dict) and isinstance(r.get("angle_start"), (int, float)) and isinstance(r.get("angle_end"), (int, float)))
    return have, len(recs)


def measure(angle):
    """角度（度）から、層10〜27の対応記載を返す。
    status：OK（1件）／OVERLAP（複数）／NO_MATCH（角度は入っているが、その角度に区分がない）／
            PARTIAL_DATA（角度が入っている区分が一部だけ。引けないのは Raw にまだ角度がないため）／
            NO_ANGLE_DATA（この層には角度が1つも入っていない）／NOT_REGISTERED（層がない）。"""
    r = _ar.process_ar_measurement(float(angle), adapted_database())
    for n, v in r["layers"].items():
        have, total = coverage(n)
        v["coverage"] = {"with_angle": have, "total": total}
        if v["status"] == "NO_MATCH" and total:
            if have == 0:
                v["status"] = "NO_ANGLE_DATA"
            elif have < total:
                v["status"] = "PARTIAL_DATA"
    return r


def verify(angle):
    """整合性の確認つき（重なり・未一致の検出）。"""
    return _scanner.verify_all_layers(float(angle), adapted_database())
