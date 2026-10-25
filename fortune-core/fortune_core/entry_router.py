"""相談内容から、4つの占い（易・タロット・風水/羅盤・四柱推命）のどれを勧めるかを決める。
単純なキーワードの規則（動きが読める・直しやすい）。迷ったらタロット。"""
from __future__ import annotations

TOOLS = {
    "shichu": "四柱推命",
    "lopan": "風水・羅盤",
    "iching": "易（梅花心易）",
    "tarot": "タロット",
}

# 先に当たったものを優先（生まれ持ったもの → 場所 → 時期・決断 → 気持ち）
RULES = [
    ("shichu", ["性格", "生まれ", "生年月日", "運命", "宿命", "適職", "天職", "才能", "人生", "大運", "年運", "相性", "命式", "四柱"]),
    ("lopan", ["方角", "方位", "風水", "引っ越し", "引越", "家", "部屋", "間取り", "土地", "玄関", "寝室", "事務所", "店", "墓", "吉方", "ベッド"]),
    ("tarot", ["気持ち", "本音", "恋", "彼", "彼女", "好き", "片思い", "復縁", "相手"]),            # 人の気持ち（強い手がかり）
    ("iching", ["いつ", "時期", "タイミング", "決断", "決める", "迷って", "どうなる", "結果", "成否", "吉凶", "試験", "契約", "勝負", "進むべき", "やめるべき", "すべきか", "べきか"]),
    ("tarot", ["関係", "心理", "悩み", "不安", "今の状況"]),                                          # 弱い手がかり（決断の言葉が無いとき）
]

REASON = {
    "shichu": "生まれ持った性質や、人生の流れを見る問いには、生年月日から読む四柱推命が向いています。",
    "lopan": "場所や方角に関わる問いには、空間の気を見る風水・羅盤が向いています。",
    "iching": "「いつ」「どうするか」という決断や時期の問いには、いまの流れを見る易が向いています。",
    "tarot": "気持ちや状況の背景を、絵柄から掘り下げたい問いには、タロットが向いています。",
}


def route(question: str) -> dict:
    q = (question or "").strip()
    found = [(t, [w for w in words if w in q]) for t, words in RULES]
    hits: dict[str, list[str]] = {}
    for t, ws in found:
        hits.setdefault(t, []).extend(ws)
    chosen = next((t for t, ws in found if ws), "tarot")
    alternatives = [t for t in TOOLS if t != chosen and hits.get(t)]
    return {
        "tool": chosen,
        "label": TOOLS[chosen],
        "reason": REASON[chosen] if hits[chosen] else "はっきりした手がかりがなかったので、まずはタロットで状況を見るのがおすすめです。",
        "matched": hits[chosen],
        "alternatives": [{"tool": t, "label": TOOLS[t]} for t in alternatives],
    }
