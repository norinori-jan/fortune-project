"""ケルト十字の鑑定文を、カードの意味から組み立てる（AI・APIキー不要）。

素材：tarot_engine の全78枚の意味（正位置・逆位置・キーワード）と、
fortune-registry/prompts の鑑定姿勢（結論から／断言型／具体的な対処を添える／吉凶で締める）。
カードごとの Nori ノート（card_notes）は空なので、書き込まれたら optional で優先できる形にしてある。
"""
from __future__ import annotations
from typing import Any

# 位置ごとの導入文（{c} = カード名＋向き）
_LEAD = {
    1: "いまの状況の核心は{c}です。",
    2: "行く手を横切る課題は{c}です。",
    3: "根底に流れているのは{c}です。ここが今の土台になっています。",
    4: "つい最近まで影響していたのは{c}です。",
    5: "あなたが心に描く最善の姿は{c}です。",
    6: "近い未来、流れは{c}の方向へ向かいます。",
    7: "あなた自身の内面は{c}を映しています。",
    8: "周囲・環境からは{c}の影響が及んでいます。",
    9: "胸の内の希望と恐れは{c}に表れています。",
    10: "このまま進んだ先の結末は{c}です。",
}
_TAIL = {
    1: "まずここを正面から受け止めることが出発点です。",
    2: "これを避けず、条件の一つとして織り込んで動いてください。",
    3: "過去を責めるのではなく、素材として使う意識で。",
    4: "すでに過ぎた流れ。引きずらず、学びだけ持ち越しましょう。",
    5: "目標を言葉にして、一歩目を決めると近づきます。",
    6: "半歩先を見て、準備を始めるのに適した時です。",
    7: "気持ちの置き所を自覚すると、判断がぶれなくなります。",
    8: "人や環境は動かせません。受け取り方と距離の取り方を整えましょう。",
    9: "希望と恐れは同じものの表裏です。恐れは具体的な対策に変えられます。",
    10: "結末は固定ではなく、ここまでの読みを活かして変えられます。",
}
# 重めのカード（流れとして注意を要するもの）
_HARD = {"major_13", "major_15", "major_16", "major_18",
         "swords_03", "swords_05", "swords_09", "swords_10", "cups_05", "pentacles_05", "wands_10"}
_SOFT_NEUTRAL = {"major_00", "major_10", "major_12", "major_14", "major_09"}
_ADV = {
    "wands": "行動と情熱の領域です。動いた分だけ手応えが返ります。",
    "cups": "感情と人間関係の領域です。心の動きを丁寧に扱ってください。",
    "swords": "思考と決断の領域です。言葉・判断・情報の扱いが鍵になります。",
    "pentacles": "仕事・お金・生活の領域です。地に足のついた積み上げが効きます。",
}


def _tone(card: dict, rev: bool) -> float:
    cid = card.get("id", "")
    t = -1.0 if cid in _HARD else (0.0 if cid in _SOFT_NEUTRAL else 1.0)
    if rev:
        t = -0.5 * t if t else 0.0
        if t == 0.0:
            t = -0.2
    return t


def _verdict(score: float) -> tuple[str, str]:
    if score >= 2.0:
        return "吉", "流れは良好です。迷わず進めて構いません。"
    if score >= 0.6:
        return "小吉", "おおむね追い風です。足元を確かめながら進めば実ります。"
    if score >= -0.6:
        return "平", "吉凶は拮抗しています。焦らず、選択を一つずつ確かめてください。"
    if score >= -2.0:
        return "吝", "渋りのある流れです。急がず、守りを固めてから動きましょう。"
    return "凶", "強い向かい風です。大きな決断は先送りし、損失を抑える手を優先してください。"


def build_reading(positions: dict[str, Any], question: str = "", notes: dict[str, str] | None = None) -> dict[str, Any]:
    """positions は draw_celtic_cross の positions。notes はカードid→自分の鑑定メモ（あれば優先）。"""
    notes = notes or {}
    per: dict[int, dict[str, Any]] = {}
    score = 0.0
    weights = {1: 1.0, 2: 0.8, 5: 0.8, 6: 1.0, 9: 0.5, 10: 1.6}
    suits: dict[str, int] = {}
    majors = 0
    revs = 0
    for p in positions.values():
        i = int(p["position_index"]); c = p.get("card") or {}; rev = bool(p.get("is_reversed"))
        name = f"{c.get('name','?')}（{'逆位置' if rev else '正位置'}）"
        body = c.get("meaning_reversed") if rev else c.get("meaning_upright")
        body = notes.get(c.get("id", "")) or body or ""
        text = _LEAD[i].format(c=name) + body + _TAIL[i]
        t = _tone(c, rev)
        score += t * weights.get(i, 0.3)
        per[i] = {"position": p.get("position_label"), "card": c.get("name"), "reversed": rev, "tone": t, "text": text}
        if c.get("arcana") == "major":
            majors += 1
        elif c.get("suit"):
            suits[c["suit"]] = suits.get(c["suit"], 0) + 1
        revs += 1 if rev else 0
    label, vtext = _verdict(score)
    ps = []
    if question:
        ps.append(f"ご相談「{question.strip()[:80]}」について、結論からお伝えします。判定は【{label}】。{vtext}")
    else:
        ps.append(f"結論からお伝えします。判定は【{label}】。{vtext}")
    f = per.get(10)
    if f:
        ps.append(f"最終の結末に出たのは{f['card']}（{'逆位置' if f['reversed'] else '正位置'}）。{'' if not f['reversed'] else '逆位置は、力が出し切れていない・向きを見直す合図です。'}")
    if majors >= 4:
        ps.append(f"大アルカナが{majors}枚。個人の努力を超えた大きな流れが働いています。目先の損得より、節目として捉えてください。")
    elif majors <= 1:
        ps.append("小アルカナが中心です。日々の選択や行動で、結果は十分に動かせます。")
    if suits:
        s = max(suits, key=lambda k: suits[k])
        if suits[s] >= 3:
            ps.append(f"{ {'wands':'ワンド','cups':'カップ','swords':'ソード','pentacles':'ペンタクル'}[s] }が{suits[s]}枚。{_ADV[s]}")
    if revs >= 6:
        ps.append("逆位置が多く、エネルギーが内に溜まっています。一度立ち止まって整えることが近道です。")
    elif revs <= 1:
        ps.append("ほぼ正位置で、力が素直に流れています。")
    ps.append("占いは判断材料のひとつです。最後に選ぶのはあなた自身です。")
    return {"verdict": label, "score": round(score, 2), "overall": "\n".join(ps), "positions": {str(k): v for k, v in per.items()}}
