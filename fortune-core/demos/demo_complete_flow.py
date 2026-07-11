"""
demo_complete_flow.py
=====================

fortune-core 縺ｮ螳悟・繝輔Ο繝ｼ 繝・Δ繝ｳ繧ｹ繝医Ξ繝ｼ繧ｷ繝ｧ繝ｳ・・
1. 蜊縺・・蜈･繧雁哨・育嶌隲・・螳ｹ蜈･蜉帚・蜊陦楢・蜍輔・繝・メ繝ｳ繧ｰ・・
2. 繧ｱ繝ｫ繝亥香蟄励せ繝励Ξ繝・ラ螳溯｡・
3. 髑大ｮ夂ｵ先棡縺ｮ繝ｬ繝昴・繝育函謌舌・菫晏ｭ・

螳溯｡梧婿豕・
    python src/fortune_core/demo_complete_flow.py
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime

_THIS_FILE = Path(__file__).resolve()
_SRC_DIR = _THIS_FILE.parent.parent
if str(_SRC_DIR) not in sys.path:
    sys.path.insert(0, str(_SRC_DIR))

from fortune_core.divination_entry import DivineEntryEngine
from fortune_core.tarot_engine import TarotEngine
from fortune_core.report_generator import ReportGenerator, ReadingReport


# ==============================================================================
# 繝・Δ逕ｨ繝ｦ繝ｼ繝・ぅ繝ｪ繝・ぅ
# ==============================================================================

def print_header(title: str):
    """繝倥ャ繝繝ｼ陦ｨ遉ｺ"""
    WIDTH = 80
    print("\n" + "=" * WIDTH)
    print(f"  {title.center(WIDTH - 4)}")
    print("=" * WIDTH + "\n")


def print_section(title: str):
    """繧ｻ繧ｯ繧ｷ繝ｧ繝ｳ陦ｨ遉ｺ"""
    print(f"\n縲・{title} 縲曾n")


def print_divider():
    """蛹ｺ蛻・ｊ邱・""
    print("-" * 80)


def safe_input(prompt: str, default: str = "") -> str:
    """螳牙・縺ｪ蜈･蜉帛叙蠕・""
    try:
        result = input(prompt)
        return result if result.strip() else default
    except (EOFError, KeyboardInterrupt):
        return default


# ==============================================================================
# 繝・Δ螳溯｡・
# ==============================================================================

def demo_complete_flow():
    """螳悟・繝輔Ο繝ｼ 繝・Δ"""
    
    print_header("醗 fortune-core 螳悟・繝輔Ο繝ｼ 繝・Δ繝ｳ繧ｹ繝医Ξ繝ｼ繧ｷ繝ｧ繝ｳ 醗")

    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    # STEP 1: 蜊縺・・蜈･繧雁哨
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    
    print_section("STEP 1・鞘Ε : 蜊縺・・蜈･繧雁哨 - 逶ｸ隲・・螳ｹ縺ｮ繝偵い繝ｪ繝ｳ繧ｰ")
    print("""
莉翫√←縺ｮ繧医≧縺ｪ縺薙→縺ｧ謔ｩ繧薙〒縺・∪縺吶°・・

縲千嶌隲・・螳ｹ縺ｮ萓九・
  窶｢ 縲御ｻ翫・繝励Ο繧ｸ繧ｧ繧ｯ繝医ｒ縺ｩ縺・ｲ繧√ｋ縺ｹ縺阪°・溘・
  窶｢ 縲・繝ｶ譛亥ｾ後・霆｢閨ｷ縺ｮ陦梧婿縺ｯ・溘・
  窶｢ 縲悟ｽｼ縺ｨ縺ｮ髢｢菫ゅ・莉雁ｾ後←縺・↑繧具ｼ溘・
  窶｢ 縲瑚・蛻・・驕ｩ閨ｷ縺ｯ菴輔°・溘・
  窶｢ 縲悟ｼ輔▲雜翫＠縺ｫ譛驕ｩ縺ｪ譁ｹ菴阪・・溘・
""")
    
    # 繧ｵ繝ｳ繝励Ν逶ｸ隲・・螳ｹ・医う繝ｳ繧ｿ繝ｩ繧ｯ繝・ぅ繝悶°蝗ｺ螳壹°・・
    sample_queries = [
        "莉翫・繝励Ο繧ｸ繧ｧ繧ｯ繝医ｒ縺ｩ縺・ｲ繧√ｋ縺ｹ縺阪°・溽憾豕√′隍・尅縺ｧ縲√メ繝ｼ繝蜀・・諢剰ｦ九ｂ蜑ｲ繧後※縺・∪縺吶・,
        "蠖ｼ縺ｨ縺ｮ髢｢菫ゅ・莉雁ｾ後←縺・↑繧翫∪縺吶°・溽ｵ仙ｩ壹ｒ閠・∴縺ｦ縺・∪縺吶′縲∝ｽｼ縺ｮ豌玲戟縺｡縺御ｸ榊ｮ峨〒縺吶・,
        "霆｢閨ｷ繧定・∴縺ｦ縺・∪縺吶′縲∵悽蠖薙↓莉翫・莨夂､ｾ繧定ｾ槭ａ繧九∋縺阪〒縺励ｇ縺・°・・,
    ]
    
    print("\n縲舌し繝ｳ繝励Ν逶ｸ隲・・螳ｹ・医ョ繝｢逕ｨ・峨・)
    for i, query in enumerate(sample_queries, 1):
        print(f"  [{i}] {query}")
    
    choice = safe_input("\n縺・★繧後°驕ｸ謚槭＠縺ｦ縺上□縺輔＞ [1-3] (繝・ヵ繧ｩ繝ｫ繝・ 1): ", "1")
    
    try:
        query_idx = int(choice) - 1
        if 0 <= query_idx < len(sample_queries):
            query_text = sample_queries[query_idx]
        else:
            query_text = sample_queries[0]
    except ValueError:
        query_text = sample_queries[0]
    
    print(f"\n笨・逶ｸ隲・・螳ｹ: 縲鶏query_text}縲構n")
    
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    # STEP 2: 蜊陦楢・蜍輔・繝・メ繝ｳ繧ｰ
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    
    print_section("STEP 2・鞘Ε : 蜊陦楢・蜍輔・繝・メ繝ｳ繧ｰ")
    print("AI縺後≠縺ｪ縺溘・逶ｸ隲・・螳ｹ繧貞・譫舌＠縲∵怙驕ｩ縺ｪ蜊陦薙ｒ蛻､螳壹＠縺ｦ縺・∪縺・..")
    time.sleep(0.5)
    
    entry_engine = DivineEntryEngine()
    entry = entry_engine.create_entry(query_text)
    recommendation = entry.recommendation
    
    print(f"\n笨・蛻・梵螳御ｺ・ｼ・)
    print(f"  繧ｫ繝・ざ繝ｪ: {entry.concern_type}")
    print(f"  謗ｨ螂ｨ蜊陦・ {recommendation.divination_type}")
    print(f"  遒ｺ蠎ｦ: {recommendation.confidence:.0%}\n")
    
    print(recommendation.reasoning + "\n")
    
    print_divider()
    print("\n" + recommendation.user_guidance + "\n")
    print_divider()
    
    # 繝輔か繝ｭ繝ｼ繧｢繝・・雉ｪ蝠・
    follow_ups = entry_engine.suggest_follow_up_questions(entry)
    if follow_ups:
        print("\n縲先ｬ｡縺ｮ繧ｹ繝・ャ繝励・)
        for i, q in enumerate(follow_ups[:2], 1):
            print(f"  {i}. {q}")
    
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    # STEP 3: 繧ｱ繝ｫ繝亥香蟄励せ繝励Ξ繝・ラ螳溯｡・
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    
    print_section("STEP 3・鞘Ε : 繧ｱ繝ｫ繝亥香蟄励せ繝励Ξ繝・ラ螳溯｡・)
    print("TarotEngine 繧貞・譛溷喧縺励※縺・∪縺・..")
    
    try:
        tarot_engine = TarotEngine()
        print("笨・繧ｨ繝ｳ繧ｸ繝ｳ蛻晄悄蛹門ｮ御ｺ・ｼ―n")
    except Exception as e:
        print(f"笨・繧ｨ繝ｩ繝ｼ: {e}")
        return
    
    # 繧ｷ繝ｳ繧ｯ繝ｭ繝九す繝・ぅ繧ｷ繝ｼ繝会ｼ育樟蝨ｨ縺ｮ繝溘Μ遘偵ち繧､繝繧ｹ繧ｿ繝ｳ繝暦ｼ・
    user_seed = int(time.time() * 1000)
    
    print(f"逶ｸ隲・・螳ｹ繧貞ｿ・↓諤昴＞豬ｮ縺九∋縺ｪ縺後ｉ縲√す繝｣繝・ヵ繝ｫ縺励∪縺・..")
    print(f"・医す繝ｳ繧ｯ繝ｭ繧ｷ繝ｼ繝・ {user_seed}・噂n")
    
    # 繧ｹ繝励Ξ繝・ラ螳溯｡・
    reading_result = tarot_engine.draw_celtic_cross(user_seed, query_text)
    
    print("笨・10譫壹・繧ｫ繝ｼ繝峨′螻暮幕縺輔ｌ縺ｾ縺励◆・―n")
    
    # 邨先棡陦ｨ遉ｺ
    print("縲舌こ繝ｫ繝亥香蟄励せ繝励Ξ繝・ラ邨先棡縲曾n")
    positions = reading_result.get("positions", {})
    
    position_labels = {
        "CURRENT_SITUATION": "竭 迴ｾ蝨ｨ縺ｮ迥ｶ豕・,
        "CROSSING_CHALLENGE": "竭｡ 隱ｲ鬘後・莠､蟾ｮ縺吶ｋ繧ゅ・",
        "DISTANT_PAST": "竭｢ 驕縺・℃蜴ｻ繝ｻ譬ｹ蠎・,
        "RECENT_PAST": "竭｣ 霑代＞驕主悉縺ｮ蠖ｱ髻ｿ",
        "BEST_OUTCOME": "竭､ 諢剰ｭ倥・譛蝟・・邨先棡",
        "IMMEDIATE_FUTURE": "竭･ 霑第悴譚･縺ｮ譁ｹ蜷第ｧ",
        "SELF_PERCEPTION": "竭ｦ 閾ｪ蟾ｱ隱崎ｭ倥・蜀・擇",
        "EXTERNAL_INFLUENCES": "竭ｧ 螟夜Κ迺ｰ蠅・・莉冶・・蠖ｱ髻ｿ",
        "HOPES_AND_FEARS": "竭ｨ 蟶梧悍縺ｨ諱舌ｌ",
        "FINAL_OUTCOME": "竭ｩ 譛邨ら噪縺ｪ邨先忰",
    }
    
    for pos_key, pos_data in positions.items():
        card = pos_data.get("card", {})
        is_reversed = pos_data.get("is_reversed", False)
        card_name = card.get("name", "Unknown")
        element = card.get("element", "?")
        meaning_key = "meaning_reversed" if is_reversed else "meaning_upright"
        meaning = card.get(meaning_key, "")
        
        label = position_labels.get(pos_key, f"? {pos_key}")
        orientation = "売 騾・ｽ咲ｽｮ" if is_reversed else "笨・豁｣菴咲ｽｮ"
        
        print(f"{label}")
        print(f"  繧ｫ繝ｼ繝・ {card_name} [{element}]")
        print(f"  蜷代″: {orientation}")
        print(f"  隗｣驥・ {meaning[:60]}...\n" if len(meaning) > 60 else f"  隗｣驥・ {meaning}\n")
    
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    # STEP 4: 隕∫ｴ繝舌Λ繝ｳ繧ｹ蛻・梵
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    
    print_section("STEP 4・鞘Ε : 隕∫ｴ繝舌Λ繝ｳ繧ｹ蛻・梵")
    
    element_dist = {}
    for pos_data in positions.values():
        card = pos_data.get("card", {})
        element = card.get("element", "unknown")
        element_dist[element] = element_dist.get(element, 0) + 1
    
    element_emojis = {
        "fire": "櫨 轣ｫ・医Ρ繝ｳ繝会ｼ・,
        "water": "挑 豌ｴ・医き繝・・・・,
        "air": "軒 鬚ｨ・医た繝ｼ繝会ｼ・,
        "earth": "諺 蝨ｰ・医・繝ｳ繧ｿ繧ｯ繝ｫ・・,
        "spirit": "笨ｨ 髴奇ｼ亥､ｧ繧｢繝ｫ繧ｫ繝奇ｼ・,
    }
    
    print("縺薙・繧ｹ繝励Ξ繝・ラ縺ｮ隕∫ｴ蛻・ｸ・\n")
    for element, count in element_dist.items():
        label = element_emojis.get(element, f"? {element}")
        bar = "笆" * count + "笆｡" * (10 - count)
        print(f"  {label:<20} {bar} ({count})")
    
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    # STEP 5: 繝ｬ繝昴・繝育函謌舌・菫晏ｭ・
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    
    print_section("STEP 5・鞘Ε : 髑大ｮ夂ｵ先棡繝ｬ繝昴・繝育函謌・)
    
    # Reading ID 逕滓・
    reading_id = f"reading_{user_seed}"
    
    # ReportData 讒狗ｯ・
    report = ReadingReport(
        reading_id=reading_id,
        query_text=query_text,
        timestamp=datetime.now().isoformat(),
        divination_type=recommendation.divination_type,
        positions=positions,
        element_distribution=element_dist,
        user_seed=user_seed,
    )
    
    # 繝ｬ繝昴・繝育函謌・
    report_generator = ReportGenerator()
    
    print("繝ｬ繝昴・繝医ｒ逕滓・縺励※縺・∪縺・..\n")
    
    try:
        export_paths = report_generator.export_formats(report, formats=("json", "html"))
        
        print("笨・繝ｬ繝昴・繝育函謌仙ｮ御ｺ・ｼ―n")
        print("縲蝉ｿ晏ｭ倥ヵ繧｡繧､繝ｫ縲・)
        for fmt, path in export_paths.items():
            print(f"  {fmt.upper()}: {path}")
        
        # JSON 繝励Ξ繝薙Η繝ｼ
        print("\n縲辱SON 繝・・繧ｿ 繝励Ξ繝薙Η繝ｼ縲曾n")
        json_str = report_generator.generate_json_report(report)
        json_obj = json.loads(json_str)
        print(json.dumps(
            {
                "reading_id": json_obj["reading_id"],
                "query_text": json_obj["query_text"],
                "timestamp": json_obj["timestamp"],
                "divination_type": json_obj["divination_type"],
                "user_seed": json_obj["user_seed"],
                "element_distribution": json_obj["element_distribution"],
                "positions": "・亥・10繝昴ず繧ｷ繝ｧ繝ｳ蛻・・繧ｫ繝ｼ繝画ュ蝣ｱ・・,
            },
            ensure_ascii=False,
            indent=2
        ))
        
    except Exception as e:
        print(f"笨・繝ｬ繝昴・繝育函謌舌お繝ｩ繝ｼ: {e}")
        return
    
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    # STEP 6: 菫晏ｭ俶婿豕輔ぎ繧､繝・
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    
    print_section("STEP 6・鞘Ε : 菫晏ｭ俶婿豕輔ぎ繧､繝・)
    
    save_guide = report_generator.get_save_instructions()
    print(save_guide)
    
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    # 螳御ｺ・
    # 笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤笏≫煤
    
    print_header("笨ｨ 繝・Δ繝ｳ繧ｹ繝医Ξ繝ｼ繧ｷ繝ｧ繝ｳ螳御ｺ・ｼ・笨ｨ")
    print(f"""
縲舌％縺ｮ繝・Δ縺ｧ螳滓ｼ斐＠縺溘ｂ縺ｮ縲・
  1・鞘Ε  蜊縺・・蜈･繧雁哨 - 逶ｸ隲・・螳ｹ縺ｮ蛻・梵縺ｨ蜊陦楢・蜍輔・繝・メ繝ｳ繧ｰ
  2・鞘Ε  繧ｱ繝ｫ繝亥香蟄励せ繝励Ξ繝・ラ - 10譫壹・繧ｫ繝ｼ繝牙ｱ暮幕
  3・鞘Ε  隕∫ｴ繝舌Λ繝ｳ繧ｹ蛻・梵 - 譚ｱ豢句頃陦馴｣謳ｺ縺ｮ蝓ｺ逶､
  4・鞘Ε  繝ｬ繝昴・繝育函謌・- JSON繝ｻHTML蠖｢蠑上〒縺ｮ螟壼ｽ｢蠑丞・蜉・
  5・鞘Ε  繝輔ぃ繧､繝ｫ菫晏ｭ・- 繝ｦ繝ｼ繧ｶ繝ｼ縺瑚・蛻・・雉・肇縺ｨ縺励※謖√■蟶ｰ繧後ｋ讖溯・

縲先ｬ｡縺ｮ繧ｹ繝・ャ繝励・
  窶｢ 繝輔Ο繝ｳ繝医お繝ｳ繝会ｼ・eb/Mobile・峨〒 UI/UX 繧呈ｧ狗ｯ・
  窶｢ 髻ｳ螢ｰ繝・く繧ｹ繝域ｳｨ蜈･讖溯・縺ｧ meanings 繧貞虚逧・↓閧ｲ謌・
  窶｢ 隍・焚蜊陦薙・騾｣謳ｺ繝ｻ繧ｯ繝ｭ繧ｹ繧ｪ繝ｼ繝舌・蛻・梵縺ｮ螳溯｣・

                醗 fortune-core 縺ｸ繧医≧縺薙◎・・醗
""")


if __name__ == "__main__":
    try:
        demo_complete_flow()
    except KeyboardInterrupt:
        print("\n\n荳ｭ譁ｭ縺励∪縺励◆縲・)
    except Exception as e:
        print(f"\n繧ｨ繝ｩ繝ｼ縺檎匱逕溘＠縺ｾ縺励◆: {e}")
        import traceback
        traceback.print_exc()
