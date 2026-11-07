"""易の辞書（真勢易秘訣・要約）の引き口。

二通りの使い方を分けて提供する。

1. 辞書引き   : lookup_dict()      卦番号・質問・分野・言葉で引く（占わない）
2. 易の解釈   : eki_reading()      占い結果（本卦・之卦）＋相談文 → 該当する占断を返す

データは eki/dict/eki_dict.csv（1行 = 卦 × 質問）。環境変数 EKI_DICT_CSV で差し替え可。
"""
from __future__ import annotations

import csv
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

_DEFAULT = Path(__file__).resolve().parents[3] / "eki" / "dict" / "eki_dict.csv"

# 相談文 → 質問ラベル（CSV の「質問」列と同じ言い方）
QUESTION_KEYWORDS: Dict[str, List[str]] = {
    "お金は入る？儲かる？": ["お金", "儲", "収入", "財", "投資", "株", "売上", "給料"],
    "結婚・縁談はうまくいく？": ["結婚", "縁談", "婚", "恋", "彼氏", "彼女", "復縁", "プロポーズ", "告白"],
    "仕事・就職・昇進はどう？": ["仕事", "転職", "就職", "昇進", "就活", "会社", "職場", "独立", "起業"],
    "引っ越していい？": ["引っ越", "引越", "転居", "住ま", "家を買", "購入", "新居"],
    "出かけていい？旅行は？": ["旅行", "出かけ", "出張", "移動", "旅", "留学", "海外"],
    "あの人は来る？": ["来る", "来てくれ", "連絡", "返事", "待ち人", "会える"],
    "なくした物は出てくる？": ["なくし", "失くし", "落とし", "紛失", "探し物", "見つか"],
    "いなくなった人はどこ？": ["行方", "家出", "いなくなっ", "失踪", "迷子", "ペットが"],
    "天気は？": ["天気", "雨", "晴れ"],
    "お産は無事？": ["お産", "出産", "安産"],
    "男の子？女の子？": ["男の子", "女の子", "性別", "胎"],
    "勝てる？": ["勝て", "勝負", "試合", "試験", "受験", "裁判", "訴訟", "選挙", "競争"],
    "体調・病気はどう？": ["体調", "病気", "病", "治", "健康", "手術", "入院", "怪我", "ケガ"],
    "交渉・取引・頼みごとはまとまる？": ["交渉", "取引", "契約", "商談", "頼み", "お願い", "借り", "貸", "話し合い"],
    "願いは叶う？": ["願い", "叶", "夢", "目標"],
    "今の運勢は？": ["運勢", "運気", "今後", "これから", "どんな時期"],
}


def _path() -> Path:
    p = os.environ.get("EKI_DICT_CSV")
    return Path(p) if p else _DEFAULT


@lru_cache(maxsize=1)
def _load() -> List[Dict[str, str]]:
    p = _path()
    if not p.exists():
        return []
    with p.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def reload() -> int:
    _load.cache_clear()
    return len(_load())


def classify_question(text: str) -> Optional[str]:
    """相談文から質問ラベルを推定する。当たらなければ None（=全体運扱いにしない）。"""
    if not text:
        return None
    best, score = None, 0
    for label, words in QUESTION_KEYWORDS.items():
        s = sum(1 for w in words if w in text)
        if s > score:
            best, score = label, s
    return best


def _row(r: Dict[str, str]) -> Dict[str, Any]:
    return {
        "question": r["質問"],
        "field": r["分野"],
        "ask": r["相談の言い方"],
        "verdict": r["判定"],
        "summary": r["一言"],
        "detail": r["内容"],
        "keywords": r["探しやすい言葉"],
        "source": r["出典"],
        "qimen_matter": r["奇門遁甲の事項"],
        "qimen_look": r["奇門で見る所"],
    }


def hexagram_entry(number: int, question: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """1卦分: 卦意 ＋（質問を指定すればその占断、なければ全占断）。"""
    rows = [r for r in _load() if r["卦番号"] == str(number)]
    if not rows:
        return None
    head = rows[0]
    meaning = next((r for r in rows if r["質問"] == "卦意"), None)
    topics = [r for r in rows if r["質問"] != "卦意"]
    if question:
        topics = [r for r in topics if r["質問"] == question]
    return {
        "number": number,
        "name": head["卦名"],
        "yomi": head["よみ"],
        "upper": head["上卦"],
        "lower": head["下卦"],
        "meaning": _row(meaning) if meaning else None,
        "topics": [_row(r) for r in topics],
    }


# ---------------------------------------------------------------- 1. 辞書引き
def lookup_dict(
    number: Optional[int] = None,
    question: Optional[str] = None,
    field: Optional[str] = None,
    word: Optional[str] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    """辞書として引く。条件は AND。占いはしない。"""
    out: List[Dict[str, Any]] = []
    for r in _load():
        if number is not None and r["卦番号"] != str(number):
            continue
        if question and r["質問"] != question:
            continue
        if field and r["分野"] != field:
            continue
        if word and word not in (r["探しやすい言葉"] + r["一言"] + r["内容"] + r["卦名"] + r["相談の言い方"]):
            continue
        d = _row(r)
        d.update(number=int(r["卦番号"]), name=r["卦名"])
        out.append(d)
    return {"count": len(out), "rows": out[:limit]}


# ---------------------------------------------------------------- 2. 易の解釈
def eki_reading(
    number: int,
    changed_number: Optional[int] = None,
    changing_lines: Optional[List[int]] = None,
    question_text: str = "",
    question_type: Optional[str] = None,
) -> Dict[str, Any]:
    """占い結果に辞書を当てる。

    本卦は卦意＋相談に該当する占断。変爻があれば之卦の占断を「変化の行き先」として添える。
    相談の種類を判別できなければ、占断は出さず卦意のみ返す（全16項目を並べて混乱させない）。
    """
    qtype = question_type or classify_question(question_text)
    changing = changing_lines or []
    main = hexagram_entry(number, qtype)
    changed = hexagram_entry(changed_number, qtype) if changed_number and changing else None
    return {
        "question_type": qtype,
        "question_type_guessed": question_type is None,
        "changing_count": len(changing),
        "main": main,
        "changed": changed,
        "note": (
            "変爻なし：本卦の占断を読む。" if not changing
            else "変爻あり：本卦の占断を基本に、之卦は変化の行き先として読む。変爻の爻辞は別途参照。"
        ),
    }
