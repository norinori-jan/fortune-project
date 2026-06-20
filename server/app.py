"""
server/app.py
fortune-project 統合 API サーバー（FastAPI）

エンドポイント:
  POST /fortune/run    - 占術実行（易・タロット・風水・四柱）
  POST /fortune/query  - AI読み解き生成（Claude API）
  GET  /fortune/health - ヘルスチェック
  GET  /fortune/tools  - 利用可能ツール一覧

起動方法:
  cd C:\\Users\\norin\\fortune-project
  uvicorn server.app:app --reload --port 8000

依存:
  pip install fastapi uvicorn anthropic python-dotenv
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# パス設定（core/ を import 可能にする）
ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "fortune-core" / "src"))

# ─────────────────────────────────────────────
# 環境変数
# ─────────────────────────────────────────────
from dotenv import load_dotenv
load_dotenv(ROOT / ".env")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# ─────────────────────────────────────────────
# FastAPI アプリ
# ─────────────────────────────────────────────
app = FastAPI(
    title="fortune-project API",
    description="易・タロット・風水・四柱推命 統合占術エンジン",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # 本番では適切に制限すること
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────
# リクエスト/レスポンス型
# ─────────────────────────────────────────────

ToolName = Literal["iching", "tarot", "lopan", "shichu", "meihua"]

class FortuneRunRequest(BaseModel):
    tool:      ToolName
    question:  str = Field(..., min_length=1, max_length=200, description="占いたい内容")
    params:    dict = Field(default_factory=dict, description="ツール固有パラメータ")
    timestamp: Optional[int] = None

class FortuneQueryRequest(BaseModel):
    tool:       ToolName
    raw_result: dict = Field(..., description="FortuneRunResponse.raw_result をそのまま渡す")
    question:   str
    language:   str = Field(default="ja", description="応答言語")

class WuxingVector(BaseModel):
    wood:  float = 0.0
    fire:  float = 0.0
    earth: float = 0.0
    metal: float = 0.0
    water: float = 0.0

class FortuneRunResponse(BaseModel):
    tool:        ToolName
    timestamp:   int
    wuxing:      WuxingVector
    raw_result:  dict
    summary:     str
    symbols:     list[str]
    time_context: dict

class FortuneQueryResponse(BaseModel):
    tool:     ToolName
    core:     str   # 核心メッセージ（50字以内）
    detail:   str   # 詳細解釈
    action:   str   # 推奨アクション
    resonance: Optional[dict] = None

# ─────────────────────────────────────────────
# レジストリ読み込み
# ─────────────────────────────────────────────

_registry_cache: Optional[dict] = None

def load_registry() -> dict:
    global _registry_cache
    if _registry_cache:
        return _registry_cache

    # 優先順位: core/ → fortune-core/docs/
    candidates = [
        ROOT / "core" / "registry_a.json",
        ROOT / "fortune-core" / "docs" / "index.json",
        ROOT / "fortune-registry" / "registry.json",
    ]
    for path in candidates:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                _registry_cache = json.load(f)
            print(f"[registry] loaded: {path}")
            return _registry_cache

    raise RuntimeError("registry_a.json が見つかりません")

# ─────────────────────────────────────────────
# 時間コンテキスト生成（timeAxis.py の Python版）
# ─────────────────────────────────────────────

TIANGAN = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DIZHI   = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
DIZHI_WX = ["water","earth","wood","wood","earth","fire",
             "fire","earth","metal","metal","earth","water"]

def get_time_context(dt: Optional[datetime] = None) -> dict:
    dt = dt or datetime.now()
    y = dt.year
    gan_idx  = (y - 4)  % 10
    zhi_idx  = (y - 4)  % 12
    day_diff = (dt.date() - datetime(2024, 1, 1).date()).days
    d_gan = TIANGAN[((day_diff % 10) + 10) % 10]
    d_zhi = DIZHI[((day_diff % 12) + 12) % 12]
    m_zhi = DIZHI[((dt.month - 1 + 2) % 12)]
    kyusei = ((11 - (y % 9)) % 9) or 9
    return {
        "yearKanshi":  f"{TIANGAN[gan_idx % 10]}{DIZHI[zhi_idx % 12]}",
        "monthKanshi": f"？{m_zhi}",
        "dayKanshi":   f"{d_gan}{d_zhi}",
        "junishi":     d_zhi,
        "yuejian":     m_zhi,
        "rizhen":      d_zhi,
        "kyusei":      kyusei,
        "kanshi":      f"{TIANGAN[gan_idx % 10]}{DIZHI[zhi_idx % 12]}",
    }

# ─────────────────────────────────────────────
# ツール別ロジック ディスパッチャ
# ─────────────────────────────────────────────

def _run_iching(question: str, params: dict, registry: dict) -> dict:
    """梅花心易・六爻占術"""
    try:
        from meihua.meihuaEngine import run as meihua_run
        result = meihua_run(question, params)
        return {"engine": "meihua", "result": result}
    except ImportError:
        pass

    # フォールバック：簡易起卦（時間数）
    import random
    now = datetime.now()
    upper = ((now.year + now.month + now.day + now.hour) % 8) or 8
    lower = ((upper + now.hour) % 8) or 8
    dong  = ((now.year + now.month + now.day + now.hour) % 6) or 6

    bagua_names = ["","乾","兌","離","震","巽","坎","艮","坤"]
    upper_name  = bagua_names[upper]
    lower_name  = bagua_names[lower]

    hexagrams = registry.get("hexagrams", {})
    # 上卦下卦からIDを検索
    bagua_ids  = ["","qian","dui","li","zhen","xun","kan","gen","kun"]
    hex_entry  = next(
        (v for v in hexagrams.values()
         if v.get("upper") == bagua_ids[upper]
         and v.get("lower") == bagua_ids[lower]),
        None
    )
    return {
        "engine":     "iching_fallback",
        "upperGua":   upper_name,
        "lowerGua":   lower_name,
        "dongYao":    dong,
        "hexName":    hex_entry["name_ja"] if hex_entry else f"{upper_name}上/{lower_name}下",
        "hexCore":    hex_entry["core"]    if hex_entry else "卦を読み解いています。",
        "hexNumber":  hex_entry["number"]  if hex_entry else 0,
    }


def _run_tarot(question: str, params: dict, registry: dict) -> dict:
    """タロット（大アルカナ3枚引き）"""
    import random
    tarot = registry.get("tarot", {})
    if not tarot:
        raise HTTPException(500, "タロットデータがレジストリに見つかりません")

    cards = list(tarot.values())
    drawn = random.sample(cards, min(3, len(cards)))
    positions = ["過去", "現在", "未来"]
    spread = []
    wuxing_acc = {"wood":0,"fire":0,"earth":0,"metal":0,"water":0}

    for i, card in enumerate(drawn):
        reversed_card = random.random() < 0.3
        spread.append({
            "position": positions[i],
            "card":     card["name_ja"],
            "name_en":  card["name_en"],
            "number":   card["number"],
            "wuxing":   card["wuxing"],
            "keywords": card["keywords"],
            "reversed": reversed_card,
            "core":     card["core"],
        })
        wx = card["wuxing"]
        if wx in wuxing_acc:
            wuxing_acc[wx] += 1

    return {
        "engine":   "tarot_major_arcana",
        "spread":   spread,
        "wuxing_raw": wuxing_acc,
    }


def _run_shichu(question: str, params: dict, registry: dict) -> dict:
    """四柱推命（簡易）"""
    try:
        from shichu.engine import run as shichu_run
        return {"engine": "shichu", "result": shichu_run(params)}
    except ImportError:
        pass

    birth = params.get("birth_date", "")
    if not birth:
        raise HTTPException(400, "四柱推命には birth_date (YYYY-MM-DD) が必要です")

    try:
        dt  = datetime.strptime(birth, "%Y-%m-%d")
        ctx = get_time_context(dt)
    except ValueError:
        raise HTTPException(400, "birth_date の形式が不正です（YYYY-MM-DD）")

    return {
        "engine":      "shichu_fallback",
        "birth":       birth,
        "yearKanshi":  ctx["yearKanshi"],
        "note":        "詳細は core/shichu/engine.py を参照",
    }


def _run_lopan(question: str, params: dict, registry: dict) -> dict:
    """風水・羅盤"""
    lopan = registry.get("lopan", {})
    lhb   = lopan.get("later_heaven_bagua", {})
    kyusei_map = lopan.get("lucky_directions_by_kyusei", {})
    ctx   = get_time_context()
    ky    = str(ctx["kyusei"])

    lucky = kyusei_map.get(ky, {})
    return {
        "engine":       "lopan",
        "kyusei":       ky,
        "best_dirs":    lucky.get("best", []),
        "avoid_dirs":   lucky.get("avoid", []),
        "directions":   lhb,
        "note":         f"今年の九星：{ky}星　吉方位：{', '.join(lucky.get('best', []))}",
    }


TOOL_DISPATCH = {
    "iching": _run_iching,
    "meihua": _run_iching,
    "tarot":  _run_tarot,
    "shichu": _run_shichu,
    "lopan":  _run_lopan,
}

def calc_wuxing(tool: str, raw: dict) -> WuxingVector:
    """生結果から五行ベクトルを計算"""
    v = {"wood":0.0,"fire":0.0,"earth":0.0,"metal":0.0,"water":0.0}

    if tool in ("iching", "meihua"):
        # 上卦・下卦の五行
        bagua_wx = {
            "qian":"metal","dui":"metal","li":"fire","zhen":"wood",
            "xun":"wood","kan":"water","gen":"earth","kun":"earth",
        }
        bagua_names = {"乾":"qian","兌":"dui","離":"li","震":"zhen",
                       "巽":"xun","坎":"kan","艮":"gen","坤":"kun"}
        for key in ("upperGua","lowerGua"):
            gname = raw.get(key,"")
            bid   = bagua_names.get(gname)
            if bid and bid in bagua_wx:
                wx = bagua_wx[bid]
                v[wx] = min(1.0, v[wx] + 0.4)

    elif tool == "tarot":
        raw_wx = raw.get("wuxing_raw", {})
        total  = sum(raw_wx.values()) or 1
        for k in v:
            v[k] = raw_wx.get(k, 0) / total

    elif tool == "shichu":
        # 年干支の五行
        wx_map = {"甲":"wood","乙":"wood","丙":"fire","丁":"fire",
                  "戊":"earth","己":"earth","庚":"metal","辛":"metal",
                  "壬":"water","癸":"water"}
        yk = raw.get("yearKanshi","")
        if yk and yk[0] in wx_map:
            v[wx_map[yk[0]]] = 0.6

    elif tool == "lopan":
        dir_wx = {"N":"water","NE":"earth","E":"wood","SE":"wood",
                  "S":"fire","SW":"earth","W":"metal","NW":"metal"}
        for d in raw.get("best_dirs", []):
            wx = dir_wx.get(d)
            if wx:
                v[wx] = min(1.0, v[wx] + 0.35)

    total = sum(v.values()) or 1
    return WuxingVector(**{k: round(val/total, 3) for k, val in v.items()})

# ─────────────────────────────────────────────
# エンドポイント
# ─────────────────────────────────────────────

@app.get("/fortune/health")
def health():
    return {
        "status": "ok",
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tools": list(TOOL_DISPATCH.keys()),
    }


@app.get("/fortune/tools")
def list_tools():
    return {
        "tools": [
            {"id":"iching",  "name":"梅花心易・六爻", "status":"available"},
            {"id":"tarot",   "name":"タロット",        "status":"available"},
            {"id":"shichu",  "name":"四柱推命",        "status":"available"},
            {"id":"lopan",   "name":"風水・羅盤",      "status":"available"},
            {"id":"meihua",  "name":"梅花心易（詳細）","status":"available"},
        ]
    }


@app.post("/fortune/run", response_model=FortuneRunResponse)
def fortune_run(req: FortuneRunRequest):
    registry   = load_registry()
    dispatcher = TOOL_DISPATCH.get(req.tool)
    if not dispatcher:
        raise HTTPException(400, f"未対応のツール: {req.tool}")

    try:
        raw = dispatcher(req.question, req.params, registry)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"占術実行エラー: {str(e)}")

    wuxing   = calc_wuxing(req.tool, raw)
    time_ctx = get_time_context()
    ts       = req.timestamp or int(datetime.now().timestamp() * 1000)

    # シンボル生成
    symbols: list[str] = []
    if req.tool in ("iching","meihua"):
        bgmap = {"乾":"☰","兌":"☱","離":"☲","震":"☳","巽":"☴","坎":"☵","艮":"☶","坤":"☷"}
        for k in ("upperGua","lowerGua"):
            g = raw.get(k,"")
            if g in bgmap:
                symbols.append(bgmap[g])
        if raw.get("hexName"):
            symbols.append(raw["hexName"])
    elif req.tool == "tarot":
        symbols = [s["card"] for s in raw.get("spread",[])]
    elif req.tool == "lopan":
        symbols = raw.get("best_dirs", [])

    summary = (
        raw.get("hexCore") or
        (raw.get("spread") and raw["spread"][1]["core"] if raw.get("spread") else None) or
        raw.get("note") or
        "占断結果を生成しました。"
    )

    return FortuneRunResponse(
        tool=req.tool,
        timestamp=ts,
        wuxing=wuxing,
        raw_result=raw,
        summary=summary,
        symbols=symbols,
        time_context=time_ctx,
    )


@app.post("/fortune/query", response_model=FortuneQueryResponse)
async def fortune_query(req: FortuneQueryRequest):
    """Claude APIを呼び出してAI読み解きを生成"""
    if not ANTHROPIC_API_KEY:
        raise HTTPException(503, "ANTHROPIC_API_KEY が設定されていません（.env を確認してください）")

    # プロンプト読み込み
    prompt_path = ROOT / "fortune-registry" / "prompts" / f"{req.tool}.json"
    if not prompt_path.exists():
        prompt_path = ROOT / "fortune-registry" / "prompts" / "base.json"

    tool_prompt = ""
    if prompt_path.exists():
        with open(prompt_path, encoding="utf-8") as f:
            pdata = json.load(f)
            tool_prompt = pdata.get("system", "")

    system_prompt = f"""あなたは東洋の伝統的な思想体系——易経・風水・陰陽五行——に精通した占術師です。
占断は「当たる・当たらない」の問題ではなく、「現在の気の流れを読み、最善の選択を導く羅針盤」として機能します。

回答時の原則：
1. 五行（木火土金水）の言語で現象を解釈する
2. 変化の方向性（動爻・流れ）を必ず示す
3. 具体的な行動指針で締める
4. 恐怖ではなく、智慧として伝える
5. 必ず以下のJSON形式のみで返答する（前置き・マークダウン不要）:
{{
  "core": "核心メッセージ（50字以内）",
  "detail": "詳細解釈（200字程度）",
  "action": "推奨アクション（100字程度）",
  "resonance": {{
    "suggestedTool": "iching|tarot|lopan のいずれか",
    "reason": "なぜそのツールを勧めるか（50字）"
  }}
}}

{tool_prompt}"""

    user_message = f"""質問: {req.question}

占術ツール: {req.tool}
占断結果: {json.dumps(req.raw_result, ensure_ascii=False, indent=2)}

上記の結果を読み解き、JSON形式で回答してください。"""

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        raw_text = response.content[0].text.strip()
        # JSONブロックの抽出
        if "```" in raw_text:
            raw_text = raw_text.split("```")[1]
            if raw_text.startswith("json"):
                raw_text = raw_text[4:]
        parsed = json.loads(raw_text)
    except json.JSONDecodeError as e:
        raise HTTPException(500, f"Claude APIの応答をJSONに変換できませんでした: {e}")
    except Exception as e:
        raise HTTPException(500, f"Claude API呼び出しエラー: {str(e)}")

    return FortuneQueryResponse(
        tool=req.tool,
        core=parsed.get("core", ""),
        detail=parsed.get("detail", ""),
        action=parsed.get("action", ""),
        resonance=parsed.get("resonance"),
    )
