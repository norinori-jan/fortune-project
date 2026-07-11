# ==============================================================================
# demo_tarot.py
# ==============================================================================
# 【TarotEngine 単体動作検証チE��、E
# src/fortune_core/tarot_engine.py と data/tarot_cards.json が正しく
# 動作するかをターミナル上で確認するため�EチE��実行スクリプト、E
#
# 実行方況E
#     # リポジトリルートかめE
#     python src/fortune_core/demo_tarot.py
#
#     # また�E fortune_core パッケージとしてインポ�Eト済みの場吁E
#     python -m fortune_core.demo_tarot
#
# 動作確認頁E��:
#     1. TarotEngine の初期匁E
#     2. タイムスタンプ（ミリ秒）をシードとして draw_celtic_cross を実衁E
#     3. ケルト十字！E0 枚）�E結果を整形表示�E�カードデザイン選択可�E�E
#     4. スプレチE��全体�E允E��刁E��E��ランスを�E析�E出劁E
# ==============================================================================

import sys
import sys
import time
from pathlib import Path

# ---------------------------------------------------------------------------
# パス解決: 直接実衁E/ パッケージ実衁Eどちらでも動くよぁE��
# ---------------------------------------------------------------------------
_THIS_FILE = Path(__file__).resolve()
_SRC_DIR   = _THIS_FILE.parent.parent   # src/
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from fortune_core.tarot_engine import TarotEngine  # noqa: E402

# ---------------------------------------------------------------------------
# 表示用定数
# ---------------------------------------------------------------------------
WIDTH      = 72
DIVIDER    = "─" * WIDTH
THICK_LINE = "╁E * WIDTH
STAR_LINE  = "☁E * WIDTH

# ケルト十孁E吁E�Eジションの意味�E�英吁EↁE日本語！E
POSITION_MEANING: dict[str, str] = {
    "present":       "現在の状況E,
    "challenge":     "課題�E交差するも�E",
    "past":          "過去の影響",
    "future":        "近未来の方向性",
    "above":         "意識�E目樁E,
    "below":         "潜在意識�E基盤",
    "advice":        "アドバイス",
    "external":      "外部環墁E�E他老E�E影響",
    "hopes_fears":   "希望と恐れ",
    "outcome":       "最終的な結末",
    # engine が別のキー名を使ぁE��合に備えた追加マッピング
    "significator":  "本人・中忁E��ーチE,
    "crossing":      "課題�E交差するも�E",
    "foundation":    "潜在意識�E基盤",
    "recent_past":   "過去の影響",
    "crowning":      "意識�E目樁E,
    "near_future":   "近未来の方向性",
    "self":          "アドバイス",
    "environment":   "外部環墁E�E他老E�E影響",
    "inner_hopes":   "希望と恐れ",
    "final_outcome": "最終的な結末",
}

# 允E��の日本語ラベル
ELEMENT_LABEL: dict[str, str] = {
    "fire":   "🔥 火�E�ワンド！E,
    "water":  "💧 水�E�カチE�E�E�E,
    "air":    "🌬 風�E�ソード！E,
    "earth":  "🌿 地�E��Eンタクル�E�E,
    "spirit": "✨ 霊（大アルカナ！E,
    "major":  "✨ 大アルカチE,
    # 日本語キーにも対忁E
    "火":     "🔥 火�E�ワンド！E,
    "水":     "💧 水�E�カチE�E�E�E,
    "風":     "🌬 風�E�ソード！E,
    "地":     "🌿 地�E��Eンタクル�E�E,
    "霁E:     "✨ 霊（大アルカナ！E,
}

BAR_MAX_WIDTH = 30

# ---------------------------------------------------------------------------
# カードデザイン定義
# ---------------------------------------------------------------------------
CARD_DESIGNS: dict[str, dict] = {
    "1": {
        "label":      "✦ クラシチE���E�Etandard�E�E,
        "border":     "─",
        "vborder":    "━E,
        "corner_tl":  "━E,
        "corner_tr":  "━E,
        "corner_bl":  "━E,
        "corner_br":  "━E,
        "deco_top":   "  �E�E✧ �E�E ",
        "deco_bot":   "  �E�E✧ �E�E ",
        "header_icon": "🃏",
        "orient_up":  "[ 正位置 ↁE]",
        "orient_rev": "[ 送E��置 ↁE]",
    },
    "2": {
        "label":      "🌙 ミスチE��チE���E�Eystic Moon�E�E,
        "border":     "╁E,
        "vborder":    "╁E,
        "corner_tl":  "╁E,
        "corner_tr":  "╁E,
        "corner_bl":  "╁E,
        "corner_br":  "╁E,
        "deco_top":   "  ☽ ✦ ☾  ",
        "deco_bot":   "  ☾ ✦ ☽  ",
        "header_icon": "🌙",
        "orient_up":  "≪ 正位置 ✦ ≫",
        "orient_rev": "≪ 送E��置 ☽ ≫",
    },
    "3": {
        "label":      "🔮 サイバ�E�E�Eyber Neon�E�E,
        "border":     "━E,
        "vborder":    "━E,
        "corner_tl":  "━E,
        "corner_tr":  "━E,
        "corner_bl":  "━E,
        "corner_br":  "━E,
        "deco_top":   "  ◁E▸▸ ◁E ",
        "deco_bot":   "  ◁E◂◂ ◁E ",
        "header_icon": "⬡",
        "orient_up":  "▲ UPRIGHT ▲",
        "orient_rev": "▼ REVERSED ▼",
    },
    "4": {
        "label":      "🌸 和風�E�Eapanese Style�E�E,
        "border":     "�E�E,
        "vborder":    "�E�E,
        "corner_tl":  "、E,
        "corner_tr":  "、E,
        "corner_bl":  "、E,
        "corner_br":  "、E,
        "deco_top":   "  ❁E✿ ❁E ",
        "deco_bot":   "  ❀ ✿ ❀  ",
        "header_icon": "🌸",
        "orient_up":  "、E正位置 、E,
        "orient_rev": "、E送E��置 、E,
    },
    "5": {
        "label":      "⚡ シンプル�E�Elain ASCII�E�E,
        "border":     "-",
        "vborder":    "|",
        "corner_tl":  "+",
        "corner_tr":  "+",
        "corner_bl":  "+",
        "corner_br":  "+",
        "deco_top":   "  * * *  ",
        "deco_bot":   "  * * *  ",
        "header_icon": ">",
        "orient_up":  "(upright)",
        "orient_rev": "(reversed)",
    },
}

# ---------------------------------------------------------------------------
# ユーチE��リチE��
# ---------------------------------------------------------------------------

def display_width(text: str) -> int:
    """全角文字を幁E2、半角を幁E1 として表示幁E��返す"""
    return sum(2 if ord(c) > 0x7F else 1 for c in text)


def center_text(text: str, width: int = WIDTH) -> str:
    """表示幁E��老E�Eしてセンタリングした斁E���Eを返す"""
    dw  = display_width(text)
    pad = max(0, width - dw)
    return " " * (pad // 2) + text + " " * (pad - pad // 2)


def ljust_display(text: str, width: int) -> str:
    """表示幁E��老E�Eした左揁E��パディングを返す"""
    pad = max(0, width - display_width(text))
    return text + " " * pad


def wrap_text(text: str, max_display_width: int = 52) -> list[str]:
    """
    全见E半角混在チE��ストを表示幁E��折り返してリストで返す、E
    バグ修正: words / current_len の未使用・未初期化を解消、E
    """
    lines:         list[str] = []
    current_line:  str       = ""
    current_width: int       = 0

    for char in str(text):
        cw = 2 if ord(char) > 0x7F else 1
        if current_width + cw > max_display_width:
            lines.append(current_line)
            current_line  = char
            current_width = cw
        else:
            current_line  += char
            current_width += cw

    if current_line:
        lines.append(current_line)

    return lines


def make_bar(ratio: float, max_width: int = BAR_MAX_WIDTH) -> str:
    filled = round(ratio * max_width)
    return "▁E * filled + "▁E * (max_width - filled)


# ---------------------------------------------------------------------------
# カードデータ正規化�E�Eict / object 両対応！E
# ---------------------------------------------------------------------------

def _getval(card, *keys):
    """card ぁEdict でもオブジェクトでも最初に靁ENone な値を返す"""
    for k in keys:
        v = card.get(k) if isinstance(card, dict) else getattr(card, k, None)
        if v is not None and v != "":
            return v
    return None


def extract_card_fields(card, index: int) -> dict:
    """card�E�Eict / オブジェクト）から表示に忁E��なフィールドをまとめて返す"""
    pos_key   = str(_getval(card, "position_key", "position") or "").lower()
    pos_name  = str(_getval(card, "position_name", "position") or f"Position {index}")
    card_name = str(_getval(card, "name", "card_name")         or "�E�不�E�E�E)
    element   = str(_getval(card, "element", "suit")           or " E)
    meaning_u = str(_getval(card, "meaning_upright", "meaning") or "")
    meaning_r = str(_getval(card, "meaning_reversed")          or "")
    keywords  = _getval(card, "keywords", "key_themes")        or ""

    if isinstance(card, dict):
        is_reversed = bool(card.get("is_reversed", card.get("reversed", False)))
    else:
        is_reversed = bool(
            getattr(card, "is_reversed", getattr(card, "reversed", False))
        )

    if isinstance(keywords, list):
        keywords = "・".join(str(k) for k in keywords)
    else:
        keywords = str(keywords)

    display_meaning = (meaning_r if (is_reversed and meaning_r) else meaning_u) or meaning_r

    return {
        "pos_key":     pos_key,
        "pos_name":    pos_name,
        "card_name":   card_name,
        "is_reversed": is_reversed,
        "element":     element,
        "keywords":    keywords,
        "meaning":     display_meaning,
    }


def resolve_position_ja(pos_key: str) -> str:
    """ポジションキーから日本語説明を引く�E�部刁E��致フォールバック付き�E�E""
    ja = POSITION_MEANING.get(pos_key, "")
    if not ja:
        for k, v in POSITION_MEANING.items():
            if k in pos_key or pos_key in k:
                return v
    return ja


# ---------------------------------------------------------------------------
# draw_celtic_cross 戻り値の正規化
# ---------------------------------------------------------------------------

def normalize_result(result) -> list:
    """
    draw_celtic_cross の戻り値めElist[card] に正規化する、E
    バグ修正: dict の全 values() をそのまま返す危険なフォールバックを除去、E
    """
    if isinstance(result, list):
        return result

    if isinstance(result, dict):
        for key in ("cards", "spread"):
            candidate = result.get(key)
            if isinstance(candidate, list) and candidate:
                return candidate
        return []

    for attr in ("cards", "spread"):
        candidate = getattr(result, attr, None)
        if isinstance(candidate, list) and candidate:
            return candidate

    return []


# ---------------------------------------------------------------------------
# カード枠描画
# ---------------------------------------------------------------------------

def draw_card(
    pos_index:   int,
    pos_name:    str,
    pos_ja:      str,
    card_name:   str,
    is_reversed: bool,
    element:     str,
    keywords:    str,
    meaning:     str,
    design:      dict,
) -> None:
    """持E��デザインでカーチE1 枚�Eをターミナルに描画する"""
    b   = design["border"]
    vb  = design["vborder"]
    tl  = design["corner_tl"]
    tr  = design["corner_tr"]
    bl  = design["corner_bl"]
    br  = design["corner_br"]
    ico = design["header_icon"]
    ori = design["orient_rev"] if is_reversed else design["orient_up"]

    # 枠の横幁E��両端のコーナ�E斁E��を除ぁE��ぶん！E
    corner_w = display_width(tl) + display_width(tr)
    fill_len = WIDTH - corner_w
    # inner 行：コーナ�E幁E+ vborder ÁE2 + 両端スペ�Eス ÁE2 = 冁E��幁E
    inner_w = WIDTH - display_width(tl) - display_width(tr) - display_width(vb) * 2 - 2

    def hline(left_corner: str, right_corner: str) -> str:
        lw  = display_width(left_corner)
        rw  = display_width(right_corner)
        rep = WIDTH - lw - rw
        return left_corner + b * rep + right_corner

    def inner_line(content: str = "") -> str:
        cw  = display_width(content)
        pad = max(0, inner_w - cw)
        return f"{vb} {content}{' ' * pad} {vb}"

    elem_label = ELEMENT_LABEL.get(element, element)

    # ── 描画 ──
    print()
    print(hline(tl, tr))
    print(inner_line(design["deco_top"]))

    pos_str = f"  {pos_index:2d}. {pos_name}"
    if pos_ja:
        pos_str += f"  /  {pos_ja}"
    print(inner_line(pos_str))
    print(inner_line())
    print(inner_line(f"{ico}  {card_name}"))
    print(inner_line(f"     {ori}"))
    print(inner_line(f"     🌊 {elem_label}"))

    if keywords:
        print(inner_line(f"     🔑 {keywords}"))

    if meaning:
        print(inner_line())
        print(inner_line("  📖 解釁E"))
        for line in wrap_text(meaning, max_display_width=inner_w - 6):
            print(inner_line(f"     {line}"))

    print(inner_line(design["deco_bot"]))
    print(hline(bl, br))


# ---------------------------------------------------------------------------
# カードデザイン選択インタラクション
# ---------------------------------------------------------------------------

def choose_design() -> dict:
    """ターミナルでチE��イン番号を�E力させ、E��択しぁEdesign dict を返す"""
    print()
    print(THICK_LINE)
    print(center_text("🎨  カードデザインを選んでください  🎨"))
    print(THICK_LINE)
    for key, d in CARD_DESIGNS.items():
        print(f"  [{key}]  {d['label']}")
    print(DIVIDER)

    while True:
        try:
            choice = input("  番号を�E力してください�E�デフォルチE 1�E�E ").strip()
        except (EOFError, KeyboardInterrupt):
            choice = ""

        if choice == "":
            choice = "1"

        if choice in CARD_DESIGNS:
            selected = CARD_DESIGNS[choice]
            print(f"  ✁E選択されたチE��イン: {selected['label']}")
            return selected

        print(f"  ⚠�E�E '{choice}' は無効です、E〜{len(CARD_DESIGNS)} の番号を�E力してください、E)


# ---------------------------------------------------------------------------
# 允E��刁E��E��ランス表示
# ---------------------------------------------------------------------------

def show_element_analysis(cards: list) -> None:
    """スプレチE��全体�E允E��刁E��E��雁E���E表示する"""
    print()
    print(STAR_LINE)
    print(center_text("📊  允E��刁E��E��ランス刁E��"))
    print(STAR_LINE)

    element_counter: dict[str, int] = {}
    for card in cards:
        if isinstance(card, dict):
            elem = card.get("element") or card.get("suit") or "不�E"
        else:
            elem = getattr(card, "element", None) or getattr(card, "suit", None) or "不�E"
        elem = str(elem).strip()
        element_counter[elem] = element_counter.get(elem, 0) + 1

    total = sum(element_counter.values())

    if total == 0:
        print("  允E��チE�Eタを取得できませんでした、E)
        return

    print()
    print(f"  スプレチE��合訁E {total} 极E)
    print()

    # ヘッダー�E��E角老E�Eで手動パディング�E�E
    print(
        f"  {ljust_display('允E��', 18)}"
        f"  {ljust_display('枚数', 6)}"
        f"  {ljust_display('割吁E, 7)}"
        f"  グラチE
    )
    print(f"  {'─' * 18}  {'─' * 6}  {'─' * 7}  {'─' * BAR_MAX_WIDTH}")

    for elem, count in sorted(element_counter.items(), key=lambda x: -x[1]):
        ratio = count / total
        pct   = ratio * 100
        label = ELEMENT_LABEL.get(elem, f"  {elem}")
        bar   = make_bar(ratio)
        print(
            f"  {ljust_display(label, 18)}"
            f"  {ljust_display(str(count) + '极E, 6)}"
            f"  {ljust_display(f'{pct:5.1f}%', 7)}"
            f"  {bar}"
        )

    # バランスコメンチE
    print()
    print(f"  {'─' * (WIDTH - 4)}")
    max_elem  = max(element_counter, key=element_counter.get)  # type: ignore[arg-type]
    max_ratio = element_counter[max_elem] / total * 100
    max_label = ELEMENT_LABEL.get(max_elem, max_elem)

    print(f"  最も多い允E��: {max_label}  ({max_ratio:.1f}%)")
    if max_ratio >= 50:
        print("  ↁE特定�E素への偏りが強く、そのチE�Eマが今回の中忁E��題です、E)
    elif max_ratio >= 30:
        print("  ↁE1つの允E��が主導的ですが、�E体的に多様なチE�Eマが混在してぁE��す、E)
    else:
        print("  ↁE吁E�E素がバランスよく刁E��E��ており、多面皁E��状況を示してぁE��す、E)

    # 大アルカナ比率チェチE��
    major_keys  = {"major", "spirit", "霁E, "大アルカチE, "Major Arcana"}
    major_count = sum(v for k, v in element_counter.items() if k in major_keys)
    if major_count > 0:
        major_pct = major_count / total * 100
        print()
        print(f"  大アルカナ比率: {major_count}极E/ {major_pct:.1f}%")
        if major_pct >= 40:
            print("  ↁE宿命皁E�E大局皁E��力が強く働ぁE��おり、E��要な転換期を示唁E��ます、E)
        else:
            print("  ↁE自由意志と宿命が程よく混在するスプレチE��です、E)


# ---------------------------------------------------------------------------
# メイン処琁E
# ---------------------------------------------------------------------------

def main() -> None:

    # ── ヘッダー ────────────────────────────────────────────────────────────
    print()
    print(THICK_LINE)
    print(center_text("🔮  fortune-core  /  TarotEngine  単体動作検証チE��  🔮"))
    print(center_text("Celtic Cross Spread   E ケルト十字スプレチE��"))
    print(THICK_LINE)

    # ── カードデザイン選抁E─────────────────────────────────────────────────
    design = choose_design()

    # ── Step 1: TarotEngine 初期匁E─────────────────────────────────────────
    print()
    print(f"{'▶ Step 1 ':─<{WIDTH}}")
    print("  TarotEngine を�E期化してぁE��ぁE..")
    try:
        engine = TarotEngine()
        print("  ✁ETarotEngine の初期化に成功しました、E)
    except Exception as exc:
        print(f"  ❁ETarotEngine の初期化に失敗しました: {exc}")
        print("\n  【確認事頁E��E)
        print("  - src/fortune_core/tarot_engine.py が存在しますか�E�E)
        print("  - src/fortune_core/data/tarot_cards.json が存在しますか�E�E)
        print("  - pip install -e . でパッケージをインスト�Eルしましたか！E)
        sys.exit(1)

    # ── Step 2: シード取征E─────────────────────────────────────────────────
    print()
    print(f"{'▶ Step 2 ':─<{WIDTH}}")
    user_seed = int(time.time() * 1000)
    print("  占ぁE��がシャチE��ルを止めた瞬間�Eタイムスタンプ！Es�E�E")
    print(f"  user_seed = {user_seed}")

    # ── Step 3: クエリ設宁E─────────────────────────────────────────────────
    print()
    print(f"{'▶ Step 3 ':─<{WIDTH}}")
    query = "こ�E占ぁE��プリケーション開発プロジェクト�E今後�E進展につぁE��"
    print(f"  相諁E�E容: 「{query}、E)

    # ── Step 4: draw_celtic_cross 実衁E─────────────────────────────────────
    print()
    print(f"{'▶ Step 4 ':─<{WIDTH}}")
    print("  ケルト十字スプレチE��を展開してぁE��ぁE..")

    # 引数バリエーションを頁E��試す！Engine のシグネチャ違いに対応！E
    result      = None
    arg_variants = [
        {"user_seed": user_seed, "query": query},
        {"seed":      user_seed, "query": query},
        {"user_seed": user_seed},
        {"seed":      user_seed},
    ]
    for kwargs in arg_variants:
        try:
            result = engine.draw_celtic_cross(**kwargs)
            print(f"  ✁Edraw_celtic_cross({', '.join(f'{k}=...' for k in kwargs)}) 成功")
            break
        except TypeError:
            continue
        except Exception as exc:
            print(f"  ❁Edraw_celtic_cross の実行中にエラーが発生しました: {exc}")
            sys.exit(1)

    if result is None:
        print("  ❁Edraw_celtic_cross を呼び出せる引数の絁E��合わせが見つかりませんでした、E)
        print("     tarot_engine.py の draw_celtic_cross シグネチャを確認してください、E)
        sys.exit(1)

    cards = normalize_result(result)

    if not cards:
        print("  ❁E結果からカードリストを取得できませんでした、E)
        print(f"     result の垁E  : {type(result)}")
        print(f"     result の冁E�� : {result!r}")
        sys.exit(1)

    print(f"  📌 取得カード枚数: {len(cards)} 极E)

    # ── Step 5: スプレチE��表示 ─────────────────────────────────────────────
    print()
    print(STAR_LINE)
    print(center_text("🃏  ケルト十字スプレチE��  結果  🃏"))
    print(center_text(f"相諁E 「{query}、E))
    print(STAR_LINE)

    for i, card in enumerate(cards, start=1):
        fields = extract_card_fields(card, i)
        pos_ja = resolve_position_ja(fields["pos_key"])
        draw_card(
            pos_index   = i,
            pos_name    = fields["pos_name"],
            pos_ja      = pos_ja,
            card_name   = fields["card_name"],
            is_reversed = fields["is_reversed"],
            element     = fields["element"],
            keywords    = fields["keywords"],
            meaning     = fields["meaning"],
            design      = design,
        )

    print()
    print(center_text(f"以上、{len(cards)} 枚�Eカードが展開されました、E))

    # ── Step 6: 允E��刁E��E��ランス刁E�� ──────────────────────────────────────
    show_element_analysis(cards)

    # ── フッター ─────────────────────────────────────────────────────────────
    print()
    print(THICK_LINE)
    print(center_text("✁E チE��実行完亁E  E TarotEngine は正常に動作してぁE��ぁE))
    print(THICK_LINE)
    print()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    main()
