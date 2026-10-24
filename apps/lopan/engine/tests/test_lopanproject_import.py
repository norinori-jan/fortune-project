"""lopanproject から取り込んだ検証エンジンが、読み込めて、基本の動きをすることを確かめる。"""
import importlib.util, pathlib

ENGINE = pathlib.Path(__file__).resolve().parents[1]

def load(rel):
    p = ENGINE / rel
    spec = importlib.util.spec_from_file_location(p.stem, p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m

def test_import_all():
    for rel in ['integrity/angle_integrity_scanner.py', 'integrity/layer_verification_engine.py',
                'integrity/integrity_report.py', 'integrity/verification_report.py', 'api/ar_api.py']:
        assert load(rel) is not None

def test_normalize_angle():
    m = load('integrity/layer_verification_engine.py')
    assert m.normalize_lopan_angle(-10) == 350
    assert m.normalize_lopan_angle(370) == 10

def test_angle_in_range_wraps_360():
    m = load('integrity/layer_verification_engine.py')
    assert m.angle_in_range(355, 350, 10)      # 360°をまたぐ区間
    assert m.angle_in_range(5, 350, 10)
    assert not m.angle_in_range(20, 350, 10)
    assert m.angle_in_range(350, 350, 10)      # start を含む


def test_service_loads_raw_and_measures():
    s = load('lopan_service.py')
    db = s.database()
    assert {10, 11, 12, 13, 14, 24, 26}.issubset(db)
    r = s.measure(330.0)
    assert r['angle'] == 330.0
    assert r['layers'][10]['status'] == 'OK'
    assert r['layers'][10]['matches'][0]['record']['raw_text'] == '辛亥'   # 326°〜332°
    assert r['layers'][11]['matches'][0]['record']['raw_text'] == '正亥'
