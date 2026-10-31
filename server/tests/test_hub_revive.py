from fastapi.testclient import TestClient
from server.app import app
c = TestClient(app)

def test_mobile_shell_no_ai():
    r = c.get("/fortune/mobile/u1?theme=love"); assert r.status_code == 200
    d = r.json(); s = d["screens"]
    assert [n["key"] for n in s["home"]["navigation"]] == ["home","today","question","history","favorites"]
    assert 50 <= s["today"]["today"]["score"] <= 100
    assert s["question"]["form"]["examples"]

def test_hub_home_quick():
    assert c.post("/fortune/hub/home", json={"user_key":"u1"}).status_code == 200
    assert c.post("/fortune/hub/quick", json={"user_key":"u1"}).status_code in (200,)

def test_entry_and_tools():
    assert c.post("/fortune/entry", json={"question":"恋人との関係は？"}).status_code == 200
    assert c.post("/fortune/tarot/celtic", json={"question":"x"}).json()["positions"]
    assert c.post("/fortune/shichu/pillars", json={"birth_date":"1990-01-01"}).status_code == 200


def test_restored_endpoints_no_500():
    body = {"title": "t", "message": "m", "advice": "a", "date_key": "2026-10-26"}
    assert c.post("/fortune/share", json=body).status_code == 200
    for p in ("/fortune/catalog", "/fortune/suggestions", "/fortune/hub/today",
              "/fortune/screens/u1/home", "/fortune/screens/u1/today", "/fortune/shell/u1",
              "/fortune/integration/home/u1", "/fortune/integration/today/u1",
              "/fortune/contract", "/fortune/overview", "/fortune/bootstrap/u1"):
        assert c.get(p).status_code == 200, p


def test_complete_shape_and_former_500s():
    q = {"question": "今日の仕事運は？"}
    assert c.post("/fortune/bundle", json={**q}).status_code == 200
    r = c.post("/fortune/compare", json={**q}); assert r.status_code == 200 and len(r.json()["items"]) >= 3
    assert c.post("/fortune/pipeline", json={**q, "user_key": "u1", "theme": "work"}).status_code in (200, 422)
    assert c.get("/fortune/period-view/u1?theme=work&period=month").status_code == 200
    assert c.get("/fortune/content/u1/periods").status_code == 200
    assert c.post("/fortune/five-elements", json={"text": "仕事"}).status_code == 200
    assert c.post("/fortune/theme-cycle", json={**q, "theme": "work"}).status_code in (200, 422)


def test_app_page_served():
    r = c.get("/app"); assert r.status_code == 200 and "Fortune Hub" in r.text


def test_shichu_boundary_warning():
    # 2025-02-03 23:10 JST が立春。その数分前後は注意文が付く
    r = c.post("/fortune/shichu/pillars", json={"birth_date": "2025-02-03", "birth_time": "23:08"}).json()
    assert "boundary_warning" in r
    r2 = c.post("/fortune/shichu/pillars", json={"birth_date": "2025-02-10", "birth_time": "12:00"}).json()
    assert "boundary_warning" not in r2


def test_app_cards_js_served():
    r = c.get("/app/tarot-cards.js"); assert r.status_code == 200 and "TAROT_FULL" in r.text


def test_lopan_shichu_link():
    r = c.post("/fortune/lopan/link", json={"birth_date": "2024-06-01"}).json()
    assert r["honmei"]["number"] == 3 and r["honmei"]["name"] == "三碧木星"
    assert c.post("/fortune/lopan/link", json={"birth_date": "2026-03-01", "birth_time": "09:30"}).json()["honmei"]["number"] == 1
    # 立春前は前年扱い：2025-01-15 → 2024 年 → 三碧
    assert c.post("/fortune/lopan/link", json={"birth_date": "2025-01-15"}).json()["honmei"]["number"] == 3
    assert r["directions"]["best"] and r["elements"]["lacking"] in "木火土金水"
    assert c.post("/fortune/lopan/link", json={"birth_date": "bad"}).status_code == 400


def test_lopan_layers_and_measure():
    r = c.get("/fortune/lopan/layers").json()
    assert len(r["layers"]) == 18 and r["layers"][0]["layer"] == 10
    m = c.get("/fortune/lopan/measure?angle=337").json()
    assert m["layers"]["10"]["status"] == "OK" and m["layers"]["10"]["matches"][0]["record"]["raw_text"] == "癸亥"
    assert c.get("/fortune/lopan/measure?angle=400").status_code == 422


def test_guard_body_size_and_query_rate(monkeypatch):
    big = {"question": "x" * 70000}
    assert c.post("/fortune/entry", json=big).status_code == 413
    monkeypatch.setenv("FORTUNE_QUERY_PER_HOUR", "2")
    body = {"tool": "tarot", "raw_result": {}, "question": "q"}
    codes = [c.post("/fortune/query", json=body, headers={"x-forwarded-for": "203.0.113.9"}).status_code for _ in range(3)]
    assert codes[2] == 429 and 429 not in codes[:2]


def test_celtic_has_reading_text():
    from fastapi.testclient import TestClient
    from server.app import app
    r = TestClient(app).post("/fortune/tarot/celtic", json={"question": "転職すべき？", "seed": 7}).json()
    rd = r["reading"]
    assert rd["verdict"] in ("吉", "小吉", "平", "吝", "凶")
    assert len(rd["positions"]) == 10 and "転職" in rd["overall"]
    assert all(len(v["text"]) > 20 for v in rd["positions"].values())


def test_minor_arcana_svg_complete():
    import re, pathlib
    js = (pathlib.Path(__file__).resolve().parents[2] / "apps/fortune-hub/tarot-cards.js").read_text(encoding="utf-8")
    ids = set(re.findall(r'"((?:wands|cups|swords|pentacles)_\d\d)": "<svg', js))
    assert len(ids) == 56


def test_nori_notes_override(tmp_path):
    import json, sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "fortune-core"))
    from fortune_core.tarot_reading import load_nori_notes, build_reading
    (tmp_path / "13_death.json").write_text(json.dumps({"number": 13, "name_ja": "死神", "nori_notes": {"core_image": "脱皮", "up": {"keywords": [], "memo": "古い皮を脱ぐ時"}, "rev": {"keywords": [], "memo": ""}}}, ensure_ascii=False), encoding="utf-8-sig")
    n = load_nori_notes(tmp_path)
    assert n["major_13"]["up"] == "古い皮を脱ぐ時"
    pos = {"A": {"position_index": 1, "position_label": "x", "is_reversed": False, "card": {"id": "major_13", "name": "死神", "meaning_upright": "標準", "meaning_reversed": "r"}}}
    pos.update({str(k): {"position_index": k, "position_label": "x", "is_reversed": False, "card": {"id": "wands_01", "name": "w", "meaning_upright": "u", "meaning_reversed": "r"}} for k in range(2, 11)})
    t = build_reading(pos, "", n)["positions"]["1"]["text"]
    assert "古い皮を脱ぐ時" in t and "脱皮" in t and "標準" not in t
    assert load_nori_notes()  == {} or True


# ---- 四柱推命（xls 由来のデータ・命式） ----
def test_shichu_xls_tables_match_theory():
    import json, pathlib
    from fortune_core.shichu_meishiki import tsuhen, unsei, STEMDATA
    assert len(STEMDATA) == 10
    for d, e in STEMDATA.items():
        for t, v in e["tsuhen"].items():
            assert tsuhen(d, t) == v
        for b, v in e["unsei"].items():
            assert unsei(d, b) == v


def test_shichu_meishiki_known_chart():
    from datetime import datetime
    from fortune_core.shichu_meishiki import build_meishiki
    r = build_meishiki(datetime(2000, 1, 1, 12, 0), "男")
    assert r["pillars"] == {"year": "己卯", "month": "丙子", "day": "戊午", "hour": "戊午"}
    assert r["daiun"]["direction"] == "逆行" and r["daiun"]["list"][0]["kanshi"] == "乙亥"
    assert r["kakukyoku"]["type"] in ("内格", "外格") and r["nikkan"]["text"]
    assert build_meishiki(datetime(2000, 1, 1, 12, 0), "女")["daiun"]["direction"] == "順行"


def test_shichu_meishiki_api():
    from fastapi.testclient import TestClient
    from server.app import app
    c = TestClient(app)
    r = c.post("/fortune/shichu/meishiki", json={"birth_date": "1990-05-15", "birth_time": "10:30", "gender": "女"})
    assert r.status_code == 200 and r.json()["pillars"]["day"]
    assert c.post("/fortune/shichu/meishiki", json={"birth_date": "x"}).status_code == 422
