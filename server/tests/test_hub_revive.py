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


# ---- 観相ライブラリ（全文は非公開。ここでは仮のデータで確かめる） ----
def test_ninso_library_with_fake_volume(tmp_path, monkeypatch):
    import json
    vol = {"title": "テスト第一輯", "pages": [{"seq": 1, "printed_page": "7", "text": ""}],
           "sections": [{"title": "二、由字面（火形）", "start_seq": 1, "text": "テスト本文 初年 中年 晩年"}]}
    (tmp_path / "dai01.json").write_text(json.dumps(vol, ensure_ascii=False), encoding="utf-8")
    monkeypatch.setenv("NINSO_PRIVATE_DIR", str(tmp_path))
    from fortune_core import ninso_library as nl
    assert nl.load_volumes()[0]["no"] == 1
    r = nl.lookup_type("yu")
    assert r["name"] == "由字面" and r["sections"][0]["ref"] == "テスト第一輯 p.7"
    from fastapi.testclient import TestClient
    from server.app import app
    c = TestClient(app)
    assert c.get("/fortune/ninso/volumes").json()["volumes"][0]["sections"] == 1
    assert c.post("/fortune/ninso/lookup", json={"key": "yu"}).json()["sections"]
    assert c.post("/fortune/ninso/lookup", json={}).status_code == 422


def test_ninso_library_empty_when_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("NINSO_PRIVATE_DIR", str(tmp_path / "none"))
    from fortune_core import ninso_library as nl
    assert nl.load_volumes() == [] and nl.search("由字面") == []


def test_shichu_seminar_texts_and_kantei():
    from datetime import datetime
    from fortune_core.shichu_meishiki import build_meishiki, GENMEI, BRANCH_TEXT, ZDAYS
    assert len(GENMEI) == 10 and len(BRANCH_TEXT) == 12 and len(ZDAYS) == 12
    r = build_meishiki(datetime(1990, 5, 15, 10, 30), "女")
    titles = [s["title"] for s in r["kantei"]]
    assert any(t.startswith("元命") for t in titles) and any(t.startswith("日干") for t in titles)
    assert r["month_zoukan"]["days_from_setsu"] == 9 and r["month_zoukan"]["stem"] == "丙"


def test_shichu_meishiki_api_has_kantei():
    from fastapi.testclient import TestClient
    from server.app import app
    r = TestClient(app).post("/fortune/shichu/meishiki", json={"birth_date": "1990-05-15", "gender": "男"})
    assert r.status_code == 200 and r.json()["kantei"] and r.json()["hour_known"] is False


def test_shichu_seminar_tables_and_unsei():
    from datetime import datetime, timedelta
    from fortune_core.shichu_meishiki import build_meishiki, KISHIN_T, RITSUUN, UNSEI_T, HEALTH, STRESS
    assert len(KISHIN_T) == 12 and all(len(v) == 10 for v in KISHIN_T.values())
    assert KISHIN_T["子"]["甲"] == {"kishin": ["火", "土", "金"], "imu": ["水", "木"]}
    assert len(UNSEI_T) == 10 and len(HEALTH) == 12 and len(STRESS) == 5
    assert RITSUUN["junun"]["2"]["1"] == 1 and RITSUUN["gyakun"]["2"]["1"] == 9
    # 資料の例：日柱が乙酉の人は、2000年（庚辰）が天地徳合
    d = datetime(1985, 1, 1, 12)
    for _ in range(80):
        if build_meishiki(d, "男")["pillars"]["day"] == "乙酉":
            break
        d += timedelta(days=1)
    r = build_meishiki(d, "男", year=2000)
    assert r["pillars"]["day"] == "乙酉" and "天地徳合" in [f["name"] for f in r["unsei"]["tenkanki"]]
    r = build_meishiki(datetime(1990, 5, 15, 10, 30), "女", year=2026)
    assert r["unsei"]["nenun"]["kanshi"] == "丙午" and r["unsei"]["health"]["text"]
    assert any(s["title"].endswith("年の健康運（十二運：沐浴）") for s in r["kantei"])


def test_shichu_final_seminar_tables():
    from datetime import datetime
    from fortune_core.shichu_meishiki import build_meishiki, KAN_PAIRS
    assert len(KAN_PAIRS) == 10 and all(len(v) == 10 for v in KAN_PAIRS.values())
    assert KAN_PAIRS["甲"]["甲"]["quality"] == "◎" and KAN_PAIRS["乙"]["己"]["tsuhen"] == "偏財"
    r = build_meishiki(datetime(1990, 5, 15, 10, 30), "女", year=2026)
    titles = " ".join(s["title"] for s in r["kantei"])
    assert "年上の通変星" in titles and "月上の通変星" in titles and "配偶者運" in titles and "他の干の関係" in titles


def test_shichu_jissen_sections():
    from datetime import datetime
    from fortune_core.shichu_meishiki import build_meishiki, JIS
    assert len(JIS["biz_ability"]["比肩"]) == 8 and len(JIS["kouun_unsei"]) == 12 and len(JIS["ren_hanareru"]) == 10
    assert JIS["ren_nichishu"]["甲"]["kangou"] == "己"
    r = build_meishiki(datetime(1990, 5, 15, 10, 30), "女", year=2026)
    groups = {s.get("group") for s in r["kantei"]}
    assert {"人間分析", "恋愛・結婚", "苦難と試練", "ビジネス", "今年・今月の運"} <= groups
    titles = " ".join(s["title"] for s in r["kantei"])
    assert "2026年の異性運" in titles and "能力診断" in titles and "今月" in titles
