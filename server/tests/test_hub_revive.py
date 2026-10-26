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
