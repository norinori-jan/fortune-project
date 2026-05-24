"""
registry_a.py
registry_a.json を生成するスクリプト。
このファイルが唯一の真実（SSOT）の管理者。

実行方法:
  cd C:\\Users\\norin\\fortune-project\\core
  python registry_a.py

出力: core/registry_a.json
"""

import json
import os
from datetime import datetime, timezone

# ─────────────────────────────────────────────
# 六十四卦データ
# 既存: fortune-core/src/fortune_core/data/hexagrams.json
# ─────────────────────────────────────────────

HEXAGRAMS = [
    # (番号, 上卦, 下卦, 和名, 読み, 核心メッセージ)
    (1,  "qian", "qian", "乾為天",   "けんいてん",   "創造と力強さ。天の徳に倣い積極的に進め。"),
    (2,  "kun",  "kun",  "坤為地",   "こんいち",     "受容と柔順。大地の如く万物を養い育てよ。"),
    (3,  "zhen", "kan",  "水雷屯",   "すいらいちゅん","創業の難。艱難を乗り越えれば前途は開ける。"),
    (4,  "gen",  "kan",  "山水蒙",   "さんすいもう",  "未熟と教育。謙虚に学ぶ姿勢が知恵を育む。"),
    (5,  "qian", "kan",  "水天需",   "すいてんじゅ",  "待機の時。焦らず時を待て、機は必ず来る。"),
    (6,  "kan",  "qian", "天水訟",   "てんすいしょう","争いを避けよ。和解こそが真の勝利。"),
    (7,  "kan",  "kun",  "地水師",   "ちすいし",     "統率と規律。正しい指導者の下に衆心を集めよ。"),
    (8,  "kun",  "kan",  "水地比",   "すいちひ",     "親和と連帯。志を同じくする者と手を結べ。"),
    (9,  "xun",  "qian", "風天小畜", "ふうてんしょうちく","小さな蓄積。今は力を蓄える時。"),
    (10, "qian", "dui",  "天沢履",   "てんたくり",   "礼節を守る。虎の尾を踏むような慎重さで。"),
    (11, "kun",  "qian", "地天泰",   "ちてんたい",   "太平と繁栄。天地の気が交わり万物が栄える。"),
    (12, "qian", "kun",  "天地否",   "てんちひ",     "停滞と閉塞。時節を待ち力を温存せよ。"),
    (13, "qian", "li",   "天火同人", "てんかどうじん","志を同じくする仲間との協力が道を開く。"),
    (14, "li",   "qian", "火天大有", "かてんたいゆう","大いなる豊かさ。徳をもって衆人を導け。"),
    (15, "kun",  "gen",  "地山謙",   "ちさんけん",   "謙虚さが真の強さ。高ぶらず低く保て。"),
    (16, "zhen", "kun",  "雷地豫",   "らいちよ",     "喜びと準備。万全の備えが歓喜をもたらす。"),
    (17, "dui",  "zhen", "沢雷随",   "たくらいずい",  "柔軟に従う。時の流れに乗ることが吉。"),
    (18, "gen",  "xun",  "山風蠱",   "さんぷうこ",   "腐敗を正す。過去の問題に真摯に向き合え。"),
    (19, "kun",  "dui",  "地沢臨",   "ちたくりん",   "進歩と臨近。積極的に前進する好機。"),
    (20, "xun",  "kun",  "風地観",   "ふうちかん",   "観察と洞察。広く見渡して真理を見抜け。"),
    (21, "li",   "zhen", "火雷噬嗑", "からいぜいこう","障害を噛み砕く。毅然とした決断が必要。"),
    (22, "gen",  "li",   "山火賁",   "さんかひ",     "外見の美しさ。形式よりも本質を大切に。"),
    (23, "gen",  "kun",  "山地剥",   "さんちはく",   "剥ぎ取られる時。無理に動かず耐え忍べ。"),
    (24, "kun",  "zhen", "地雷復",   "ちらいふく",   "一陽来復。新たな始まりの種が芽吹く。"),
    (25, "qian", "zhen", "天雷无妄", "てんらいむぼう","無為自然。作意なく誠実に行動せよ。"),
    (26, "gen",  "qian", "山天大畜", "さんてんたいちく","大きな蓄積。知識と経験を深める好機。"),
    (27, "gen",  "zhen", "山雷頤",   "さんらいい",   "養育と節制。何を口にし何を語るか慎め。"),
    (28, "dui",  "xun",  "沢風大過", "たくふうたいか","過剰な負荷。中心軸を保ち崩壊を防げ。"),
    (29, "kan",  "kan",  "坎為水",   "かんいすい",   "重なる困難。信念を持って深淵を渡れ。"),
    (30, "li",   "li",   "離為火",   "りいか",       "明晰な知性。附着することで光輝く。"),
    (31, "dui",  "gen",  "沢山咸",   "たくさんかん",  "感応と恋愛。心が触れ合う喜びを大切に。"),
    (32, "zhen", "xun",  "雷風恒",   "らいふうこう",  "恒常と持続。変わらぬ誠実さが道を拓く。"),
    (33, "qian", "gen",  "天山遯",   "てんさんとん",  "賢明な退却。退くことが次の前進を準備する。"),
    (34, "zhen", "qian", "雷天大壮", "らいてんたいそう","力の盛り。勢いに任せず礼を忘れるな。"),
    (35, "li",   "kun",  "火地晋",   "かちしん",     "昇進と前進。明るく進む勢いが吉を招く。"),
    (36, "kun",  "li",   "地火明夷", "ちかめいい",   "光が傷つく時。内なる明知を保ちつつ耐えよ。"),
    (37, "xun",  "li",   "風火家人", "ふうかかじん",  "家族の和。各自の役割を果たすことが幸福の基。"),
    (38, "li",   "dui",  "火沢睽",   "かたくけい",   "対立と乖離。小事においては吉、大事は慎め。"),
    (39, "kan",  "gen",  "水山蹇",   "すいさんけん",  "進路の障害。助けを求め共に難を超えよ。"),
    (40, "zhen", "kan",  "雷水解",   "らいすいかい",  "解放と緩和。障害が取り除かれ前途が開ける。"),
    (41, "gen",  "dui",  "山沢損",   "さんたくそん",  "損なうことで益を得る。誠実さが真の利益。"),
    (42, "xun",  "zhen", "風雷益",   "ふうらいえき",  "増益と発展。上が下を益するとき万物栄える。"),
    (43, "dui",  "qian", "沢天夬",   "たくてんかい",  "決断と排除。小人を断ち切る強い意志を持て。"),
    (44, "qian", "xun",  "天風姤",   "てんふうこう",  "出会いと誘惑。強い意志で流れに飲まれるな。"),
    (45, "dui",  "kun",  "沢地萃",   "たくちすい",   "集合と集中。人材と資源を一堂に集めよ。"),
    (46, "kun",  "xun",  "地風升",   "ちふうしょう",  "上昇と成長。着実な努力が高みへと導く。"),
    (47, "dui",  "kan",  "沢水困",   "たくすいこん",  "困窮の時。言葉よりも行動で誠実さを示せ。"),
    (48, "kan",  "xun",  "水風井",   "すいふうせい",  "井戸の如く。深く掘り下げ源泉を涵養せよ。"),
    (49, "dui",  "li",   "沢火革",   "たくかかく",   "変革の時。旧弊を改め新しい秩序を作れ。"),
    (50, "li",   "xun",  "火風鼎",   "かふうてい",   "鼎の新たな役割。賢者の知恵で国を養え。"),
    (51, "zhen", "zhen", "震為雷",   "しんいらい",   "驚きと覚醒。震えつつも礼を失わず前進せよ。"),
    (52, "gen",  "gen",  "艮為山",   "ごんいさん",   "静止と瞑想。動くべき時と止まるべき時を知れ。"),
    (53, "xun",  "gen",  "風山漸",   "ふうさんぜん",  "漸進と順序。焦らず段階を踏んで進め。"),
    (54, "zhen", "dui",  "雷沢帰妹", "らいたくきまい","不完全な関係。従うべき礼と本分を忘れるな。"),
    (55, "zhen", "li",   "雷火豊",   "らいかほう",   "豊かさの絶頂。驕らず今の充実を大切に。"),
    (56, "li",   "gen",  "火山旅",   "かさんりょ",   "旅人の孤独。謙虚に軽やかに行動せよ。"),
    (57, "xun",  "xun",  "巽為風",   "そんいふう",   "柔順に浸透する。繰り返すことで根付く。"),
    (58, "dui",  "dui",  "兌為沢",   "だいいたく",   "喜びと悦び。真の喜びは内から湧き出るもの。"),
    (59, "xun",  "kan",  "風水渙",   "ふうすいかん",  "離散と融解。心を開き固まった壁を溶かせ。"),
    (60, "kan",  "dui",  "水沢節",   "すいたくせつ",  "節制と節度。適切な限界を設けることが安全。"),
    (61, "xun",  "dui",  "風沢中孚", "ふうたくちゅうふ","内なる誠信。真実の誠実さが他者の心を動かす。"),
    (62, "zhen", "gen",  "雷山小過", "らいさんしょうか","小さな過ちを超えよ。大きな事は慎み小事に徹せ。"),
    (63, "kan",  "li",   "水火既済", "すいかきさい",  "成就の後。完成した今こそ油断を戒めよ。"),
    (64, "li",   "kan",  "火水未済", "かすいびさい",  "未完の可能性。完成への道はまだ続いている。"),
]

def build_hexagrams():
    result = {}
    for num, upper, lower, name_ja, reading, core_msg in HEXAGRAMS:
        hid = f"hex_{num:02d}"
        result[hid] = {
            "number":  num,
            "name_ja": name_ja,
            "reading": reading,
            "upper":   upper,
            "lower":   lower,
            "core":    core_msg,
            "wuxing": {
                # 上卦下卦の五行合算（簡易版、詳細は hexagram_wuxing.json）
            },
        }
    return result

# ─────────────────────────────────────────────
# タロット 大アルカナ
# 既存: fortune-core/src/fortune_core/data/tarot_cards.json
# ─────────────────────────────────────────────

MAJOR_ARCANA = [
    (0,  "愚者",       "THE FOOL",           "water", "新しい出発・可能性・無限",   "恐れずに踏み出せ。"),
    (1,  "魔術師",     "THE MAGICIAN",       "fire",  "意志・技術・実現力",        "持てる力をすべて使え。"),
    (2,  "女教皇",     "THE HIGH PRIESTESS", "water", "直感・神秘・潜在意識",      "内なる声に耳を傾けよ。"),
    (3,  "女帝",       "THE EMPRESS",        "earth", "豊穣・母性・創造",          "生命力を信じて育てよ。"),
    (4,  "皇帝",       "THE EMPEROR",        "metal", "権威・構造・リーダーシップ", "秩序と規律が基盤を作る。"),
    (5,  "法王",       "THE HIEROPHANT",     "earth", "伝統・教義・精神的指導",    "先人の知恵に学べ。"),
    (6,  "恋人",       "THE LOVERS",         "fire",  "選択・愛・調和",            "心の声に従い選べ。"),
    (7,  "戦車",       "THE CHARIOT",        "water", "勝利・意志力・突破",        "制御しながら前進せよ。"),
    (8,  "力",         "STRENGTH",           "fire",  "勇気・忍耐・内なる力",      "優しさが最強の力。"),
    (9,  "隠者",       "THE HERMIT",         "earth", "内省・孤独・知恵",          "立ち止まり自らを見よ。"),
    (10, "運命の輪",   "WHEEL OF FORTUNE",   "earth", "変化・サイクル・チャンス",  "変化の波に乗る時。"),
    (11, "正義",       "JUSTICE",            "metal", "公平・真実・法",            "真実を直視せよ。"),
    (12, "吊られた男", "THE HANGED MAN",     "water", "犠牲・新視点・待機",        "逆転の発想が道を開く。"),
    (13, "死神",       "DEATH",              "water", "終わり・変容・再生",        "古いものを手放せ。"),
    (14, "節制",       "TEMPERANCE",         "fire",  "調和・均衡・癒し",          "バランスが力を生む。"),
    (15, "悪魔",       "THE DEVIL",          "earth", "束縛・物質・欲望",          "鎖は幻だ。気づけば自由。"),
    (16, "塔",         "THE TOWER",          "fire",  "突破・崩壊・啓示",          "崩れる時が真の始まり。"),
    (17, "星",         "THE STAR",           "water", "希望・回復・インスピレーション","光を信じて歩め。"),
    (18, "月",         "THE MOON",           "water", "幻想・不安・無意識",        "霧の中でも歩み続けよ。"),
    (19, "太陽",       "THE SUN",            "fire",  "喜び・成功・活力",          "光の中で輝け。"),
    (20, "審判",       "JUDGEMENT",          "fire",  "覚醒・再生・使命",          "内なる呼び声に応えよ。"),
    (21, "世界",       "THE WORLD",          "earth", "完成・統合・達成",          "旅は完結し新たな旅へ。"),
]

def build_tarot():
    result = {}
    for num, name_ja, name_en, wuxing, keywords, core in MAJOR_ARCANA:
        tid = f"major_{num:02d}"
        result[tid] = {
            "number":   num,
            "name_ja":  name_ja,
            "name_en":  name_en,
            "wuxing":   wuxing,
            "keywords": keywords,
            "core":     core,
        }
    return result

# ─────────────────────────────────────────────
# 八宮首卦（六爻占術用）
# 既存: fortune-core/src/meihua/data/ と対応
# ─────────────────────────────────────────────

GONG_SHOU_GUA = {
    "qian": ["zi",   "yin",  "chen", "wu",   "shen", "xu"],
    "dui":  ["si",   "wei",  "you",  "hai",  "chou", "mao"],
    "li":   ["mao",  "si",   "wei",  "you",  "hai",  "chou"],
    "zhen": ["zi",   "yin",  "chen", "wu",   "shen", "xu"],
    "xun":  ["chou", "hai",  "you",  "wei",  "si",   "mao"],
    "kan":  ["yin",  "chen", "wu",   "shen", "xu",   "zi"],
    "gen":  ["chen", "yin",  "zi",   "xu",   "shen", "wu"],
    "kun":  ["wei",  "si",   "mao",  "chou", "hai",  "you"],
}

# ─────────────────────────────────────────────
# 風水・羅盤データ
# 既存: fengshui-app / fenshui_map と対応
# ─────────────────────────────────────────────

LOPAN_RINGS = {
    "later_heaven_bagua": {
        "N":  {"bagua": "kan",  "wuxing": "water", "kyusei": 1, "kanji": "坎"},
        "NE": {"bagua": "gen",  "wuxing": "earth", "kyusei": 8, "kanji": "艮"},
        "E":  {"bagua": "zhen", "wuxing": "wood",  "kyusei": 3, "kanji": "震"},
        "SE": {"bagua": "xun",  "wuxing": "wood",  "kyusei": 4, "kanji": "巽"},
        "S":  {"bagua": "li",   "wuxing": "fire",  "kyusei": 9, "kanji": "離"},
        "SW": {"bagua": "kun",  "wuxing": "earth", "kyusei": 2, "kanji": "坤"},
        "W":  {"bagua": "dui",  "wuxing": "metal", "kyusei": 7, "kanji": "兌"},
        "NW": {"bagua": "qian", "wuxing": "metal", "kyusei": 6, "kanji": "乾"},
    },
    "lucky_directions_by_kyusei": {
        # 九星ごとの吉方位（簡易版）
        "1": {"best": ["SE", "E"], "avoid": ["SW"]},
        "2": {"best": ["NE", "SW"], "avoid": ["E"]},
        "3": {"best": ["S", "N"], "avoid": ["W"]},
        "4": {"best": ["N", "S"], "avoid": ["NW"]},
        "5": {"best": ["NE", "SW"], "avoid": ["all"]},
        "6": {"best": ["W", "NW"], "avoid": ["SE"]},
        "7": {"best": ["NW", "W"], "avoid": ["E"]},
        "8": {"best": ["NE", "SW"], "avoid": ["S"]},
        "9": {"best": ["E", "SE"], "avoid": ["N"]},
    },
}

# ─────────────────────────────────────────────
# registry_a.json 生成
# ─────────────────────────────────────────────

def build_registry():
    registry = {
        "_meta": {
            "version":     "2.0.0",
            "generated":   datetime.now(timezone.utc).isoformat(),
            "description": "fortune-project 統合データレジストリ（SSOT）",
            "schema":      "fortune-registry/schema/v2",
        },
        "hexagrams":       build_hexagrams(),
        "tarot":           build_tarot(),
        "bagua":           {
            "qian": {"kanji": "乾", "symbol": "☰", "wuxing": "metal", "direction": "NW", "nature": "天"},
            "dui":  {"kanji": "兌", "symbol": "☱", "wuxing": "metal", "direction": "W",  "nature": "沢"},
            "li":   {"kanji": "離", "symbol": "☲", "wuxing": "fire",  "direction": "S",  "nature": "火"},
            "zhen": {"kanji": "震", "symbol": "☳", "wuxing": "wood",  "direction": "E",  "nature": "雷"},
            "xun":  {"kanji": "巽", "symbol": "☴", "wuxing": "wood",  "direction": "SE", "nature": "風"},
            "kan":  {"kanji": "坎", "symbol": "☵", "wuxing": "water", "direction": "N",  "nature": "水"},
            "gen":  {"kanji": "艮", "symbol": "☶", "wuxing": "earth", "direction": "NE", "nature": "山"},
            "kun":  {"kanji": "坤", "symbol": "☷", "wuxing": "earth", "direction": "SW", "nature": "地"},
        },
        "gong_shou_gua":   GONG_SHOU_GUA,
        "lopan":           LOPAN_RINGS,
                "wuxing": {
            "sheng": {"wood": "fire", "fire": "earth", "earth": "metal", "metal": "water", "water": "wood"},
            "ke":    {"wood": "earth", "earth": "water", "water": "fire", "fire": "metal", "metal": "wood"},
            "colors": {
                "wood": "#4a9e6b", "fire": "#c0392b", "earth": "#c8922a",
                "metal": "#a8b8c8", "water": "#2980b9",
            },
        },

        "shichu": {
            "stems": [
                {"kanji": "甲", "yin_yang": "yang", "wuxing": "wood", "nature": "大樹・剛直・外向的", "alias": ["こう"]},
                {"kanji": "乙", "yin_yang": "yin",  "wuxing": "wood", "nature": "草花・柔軟・内向的", "alias": ["おつ"]},
                {"kanji": "丙", "yin_yang": "yang", "wuxing": "fire", "nature": "太陽・明朗・外向的", "alias": ["へい"]},
                {"kanji": "丁", "yin_yang": "yin",  "wuxing": "fire", "nature": "灯火・繊細・内向的", "alias": ["てい"]},
                {"kanji": "戊", "yin_yang": "yang", "wuxing": "earth","nature": "山岳・安定・包容力", "alias": ["ぼ"]},
                {"kanji": "己", "yin_yang": "yin",  "wuxing": "earth","nature": "田畑・調整・実務", "alias": ["き"]},
                {"kanji": "庚", "yin_yang": "yang", "wuxing": "metal","nature": "鋼鉄・決断・突破力", "alias": ["こう"]},
                {"kanji": "辛", "yin_yang": "yin",  "wuxing": "metal","nature": "宝石・精密・美意識", "alias": ["しん"]},
                {"kanji": "壬", "yin_yang": "yang", "wuxing": "water","nature": "大河・包容・流動性", "alias": ["じん"]},
                {"kanji": "癸", "yin_yang": "yin",  "wuxing": "water","nature": "雨露・知恵・繊細", "alias": ["き"]},
            ],

            "branches": [
                {"kanji": "子", "yin_yang": "yang", "wuxing": "water", "hidden_stems": ["癸"], "nature": "始まり・胎動", "alias": ["ね"]},
                {"kanji": "丑", "yin_yang": "yin",  "wuxing": "earth", "hidden_stems": ["己","癸","辛"], "nature": "蓄え・準備", "alias": ["うし"]},
                {"kanji": "寅", "yin_yang": "yang", "wuxing": "wood",  "hidden_stems": ["甲","丙","戊"], "nature": "発芽・勢い", "alias": ["とら"]},
                {"kanji": "卯", "yin_yang": "yin",  "wuxing": "wood",  "hidden_stems": ["乙"], "nature": "成長・拡大", "alias": ["う"]},
                {"kanji": "辰", "yin_yang": "yang", "wuxing": "earth", "hidden_stems": ["戊","乙","癸"], "nature": "変化・転換", "alias": ["たつ"]},
                {"kanji": "巳", "yin_yang": "yin",  "wuxing": "fire",  "hidden_stems": ["丙","戊","庚"], "nature": "成熟・熱気", "alias": ["み"]},
                {"kanji": "午", "yin_yang": "yang", "wuxing": "fire",  "hidden_stems": ["丁","己"], "nature": "頂点・盛勢", "alias": ["うま"]},
                {"kanji": "未", "yin_yang": "yin",  "wuxing": "earth", "hidden_stems": ["己","丁","乙"], "nature": "調整・収穫前", "alias": ["ひつじ"]},
                {"kanji": "申", "yin_yang": "yang", "wuxing": "metal", "hidden_stems": ["庚","壬","戊"], "nature": "収縮・整理", "alias": ["さる"]},
                {"kanji": "酉", "yin_yang": "yin",  "wuxing": "metal", "hidden_stems": ["辛"], "nature": "完成・収穫", "alias": ["とり"]},
                {"kanji": "戌", "yin_yang": "yang", "wuxing": "earth", "hidden_stems": ["戊","辛","丁"], "nature": "守護・固め", "alias": ["いぬ"]},
                {"kanji": "亥", "yin_yang": "yin",  "wuxing": "water", "hidden_stems": ["壬","甲"], "nature": "胎動・準備", "alias": ["い"]},
            ],

            "five_elements": {
                "wood":  {"sheng": "fire", "ke": "earth", "traits": "成長・拡大・柔軟"},
                "fire":  {"sheng": "earth","ke": "metal","traits": "情熱・活動・上昇"},
                "earth": {"sheng": "metal","ke": "water","traits": "安定・調和・中心"},
                "metal": {"sheng": "water","ke": "wood", "traits": "収縮・決断・硬質"},
                "water": {"sheng": "wood", "ke": "fire", "traits": "知恵・流動・柔和"},
            },

            "ten_gods": [
                {"name": "比肩", "category": "self", "traits": "自立・競争・対等", "wuxing_relation": "same_element"},
                {"name": "劫財", "category": "self", "traits": "奪う・突破・兄弟", "wuxing_relation": "same_element_yin_yang_flip"},
                {"name": "食神", "category": "output", "traits": "創造・自由・表現", "wuxing_relation": "child_same_yin_yang"},
                {"name": "傷官", "category": "output", "traits": "批判・突破・才能", "wuxing_relation": "child_flip"},
                {"name": "偏財", "category": "wealth", "traits": "柔軟・社交・流動", "wuxing_relation": "money_same_yin_yang"},
                {"name": "正財", "category": "wealth", "traits": "安定・誠実・蓄積", "wuxing_relation": "money_flip"},
                {"name": "偏官", "category": "power",  "traits": "行動・刺激・挑戦", "wuxing_relation": "control_same_yin_yang"},
                {"name": "正官", "category": "power",  "traits": "秩序・責任・規律", "wuxing_relation": "control_flip"},
                {"name": "偏印", "category": "resource","traits": "直感・柔軟・精神性", "wuxing_relation": "parent_same_yin_yang"},
                {"name": "印綬", "category": "resource","traits": "学習・保護・吸収", "wuxing_relation": "parent_flip"},
            ],

            "twelve_growth": [
                {"name": "長生", "traits": "誕生・成長の始まり", "strength": "strong"},
                {"name": "沐浴", "traits": "浄化・魅力・変化", "strength": "medium"},
                {"name": "冠帯", "traits": "成熟・発展・自信", "strength": "strong"},
                {"name": "建禄", "traits": "安定・力・基盤", "strength": "strong"},
                {"name": "帝旺", "traits": "最盛期・支配・強勢", "strength": "very_strong"},
                {"name": "衰",   "traits": "減退・調整・静寂", "strength": "weak"},
                {"name": "病",   "traits": "不調・停滞・慎重", "strength": "weak"},
                {"name": "死",   "traits": "終息・手放し", "strength": "very_weak"},
                {"name": "墓",   "traits": "蓄積・内省・準備", "strength": "medium"},
                {"name": "絶",   "traits": "断絶・リセット", "strength": "very_weak"},
                {"name": "胎",   "traits": "胎動・準備", "strength": "medium"},
                {"name": "養",   "traits": "育成・保護", "strength": "medium"},
            ],

            "relations": {
                "branch_relations": {
                    "sanhe": [
                        ["申", "子", "辰"],
                        ["亥", "卯", "未"],
                        ["寅", "午", "戌"],
                        ["巳", "酉", "丑"]
                    ],
                    "liuhe": [
                        ["子", "丑"],
                        ["寅", "亥"],
                        ["卯", "戌"],
                        ["辰", "酉"],
                        ["巳", "申"],
                        ["午", "未"]
                    ],
                    "chong": [
                        ["子", "午"],
                        ["丑", "未"],
                        ["寅", "申"],
                        ["卯", "酉"],
                        ["辰", "戌"],
                        ["巳", "亥"]
                    ]
                },
                "stem_relations": {
                    "sheng": {"甲": "丙", "丙": "戊", "戊": "庚", "庚": "壬", "壬": "甲"},
                    "ke":    {"甲": "戊", "戊": "壬", "壬": "丙", "丙": "庚", "庚": "甲"}
                }
            },

                    "sixty_kanchi": [
            {"name": "甲子", "wuxing": "water", "traits": "新しい始まり・柔軟"},
            {"name": "乙丑", "wuxing": "earth", "traits": "安定・調整"},
            {"name": "丙寅", "wuxing": "wood", "traits": "成長・勢い"},
            {"name": "丁卯", "wuxing": "wood", "traits": "調和・発展"},
            {"name": "戊辰", "wuxing": "earth", "traits": "変化・転換"},
            {"name": "己巳", "wuxing": "fire", "traits": "成熟・熱気"},
            {"name": "庚午", "wuxing": "fire", "traits": "頂点・強勢"},
            {"name": "辛未", "wuxing": "earth", "traits": "調整・収穫前"},
            {"name": "壬申", "wuxing": "metal", "traits": "整理・収縮"},
            {"name": "癸酉", "wuxing": "metal", "traits": "完成・収穫"},

            {"name": "甲戌", "wuxing": "earth", "traits": "守護・固め"},
            {"name": "乙亥", "wuxing": "water", "traits": "胎動・準備"},
            {"name": "丙子", "wuxing": "water", "traits": "柔軟・流動"},
            {"name": "丁丑", "wuxing": "earth", "traits": "安定・調整"},
            {"name": "戊寅", "wuxing": "wood", "traits": "成長・勢い"},
            {"name": "己卯", "wuxing": "wood", "traits": "調和・発展"},
            {"name": "庚辰", "wuxing": "earth", "traits": "変化・転換"},
            {"name": "辛巳", "wuxing": "fire", "traits": "成熟・熱気"},
            {"name": "壬午", "wuxing": "fire", "traits": "頂点・強勢"},
            {"name": "癸未", "wuxing": "earth", "traits": "調整・収穫前"},

            {"name": "甲申", "wuxing": "metal", "traits": "整理・収縮"},
            {"name": "乙酉", "wuxing": "metal", "traits": "完成・収穫"},
            {"name": "丙戌", "wuxing": "earth", "traits": "守護・固め"},
            {"name": "丁亥", "wuxing": "water", "traits": "胎動・準備"},
            {"name": "戊子", "wuxing": "water", "traits": "柔軟・流動"},
            {"name": "己丑", "wuxing": "earth", "traits": "安定・調整"},
            {"name": "庚寅", "wuxing": "wood", "traits": "成長・勢い"},
            {"name": "辛卯", "wuxing": "wood", "traits": "調和・発展"},
            {"name": "壬辰", "wuxing": "earth", "traits": "変化・転換"},
            {"name": "癸巳", "wuxing": "fire", "traits": "成熟・熱気"},

            {"name": "甲午", "wuxing": "fire", "traits": "頂点・強勢"},
            {"name": "乙未", "wuxing": "earth", "traits": "調整・収穫前"},
            {"name": "丙申", "wuxing": "metal", "traits": "整理・収縮"},
            {"name": "丁酉", "wuxing": "metal", "traits": "完成・収穫"},
            {"name": "戊戌", "wuxing": "earth", "traits": "守護・固め"},
            {"name": "己亥", "wuxing": "water", "traits": "胎動・準備"},
            {"name": "庚子", "wuxing": "water", "traits": "柔軟・流動"},
            {"name": "辛丑", "wuxing": "earth", "traits": "安定・調整"},
            {"name": "壬寅", "wuxing": "wood", "traits": "成長・勢い"},
            {"name": "癸卯", "wuxing": "wood", "traits": "調和・発展"},

            {"name": "甲辰", "wuxing": "earth", "traits": "変化・転換"},
            {"name": "乙巳", "wuxing": "fire", "traits": "成熟・熱気"},
            {"name": "丙午", "wuxing": "fire", "traits": "頂点・強勢"},
            {"name": "丁未", "wuxing": "earth", "traits": "調整・収穫前"},
            {"name": "戊申", "wuxing": "metal", "traits": "整理・収縮"},
            {"name": "己酉", "wuxing": "metal", "traits": "完成・収穫"},
            {"name": "庚戌", "wuxing": "earth", "traits": "守護・固め"},
            {"name": "辛亥", "wuxing": "water", "traits": "胎動・準備"},
            {"name": "壬子", "wuxing": "water", "traits": "柔軟・流動"},
            {"name": "癸丑", "wuxing": "earth", "traits": "安定・調整"},

            {"name": "甲寅", "wuxing": "wood", "traits": "成長・勢い"},
            {"name": "乙卯", "wuxing": "wood", "traits": "調和・発展"},
            {"name": "丙辰", "wuxing": "earth", "traits": "変化・転換"},
            {"name": "丁巳", "wuxing": "fire", "traits": "成熟・熱気"},
            {"name": "戊午", "wuxing": "fire", "traits": "頂点・強勢"},
            {"name": "己未", "wuxing": "earth", "traits": "調整・収穫前"},
            {"name": "庚申", "wuxing": "metal", "traits": "整理・収縮"},
            {"name": "辛酉", "wuxing": "metal", "traits": "完成・収穫"},
            {"name": "壬戌", "wuxing": "earth", "traits": "守護・固め"},
            {"name": "癸亥", "wuxing": "water", "traits": "胎動・準備"}
        ]

        },
    }
    return registry



if __name__ == "__main__":
    registry = build_registry()
    out_path = os.path.join(os.path.dirname(__file__), "registry_a.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)

    hex_count  = len(registry["hexagrams"])
    tarot_count = len(registry["tarot"])
    print(f"✅ registry_a.json 生成完了")
    print(f"   六十四卦: {hex_count} 件")
    print(f"   タロット: {tarot_count} 件")
    print(f"   出力先: {out_path}")
# core/registry_a.py の末尾に追加

def load_registry():
    """registry_a.json を読み込んで返す"""
    path = os.path.join(os.path.dirname(__file__), "registry_a.json")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
