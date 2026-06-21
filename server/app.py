"""
server/app.py — Render デプロイ対応版（Claude / Gemini / OpenAI 対応）
"""

import sys, os, json
from pathlib import Path
from datetime import datetime, timezone
from typing import Optional, Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core"))
sys.path.insert(0, str(ROOT / "fortune-core" / "src"))

from dotenv import load_dotenv
load_dotenv(ROOT / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
GEMINI_API_KEY    = os.getenv("GEMINI_API_KEY",    "")
OPENAI_API_KEY    = os.getenv("OPENAI_API_KEY",    "")

app = FastAPI(
    title="fortune-project API",
    description="易・タロット・風水・四柱推命 統合占術エンジン（Claude / Gemini / OpenAI 対応）",
    version="2.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://norinori-jan.github.io","http://localhost:8000",
                   "http://localhost:3000","http://127.0.0.1:8000","null"],
    allow_origin_regex=r"https://.*\.github\.io",
    allow_methods=["GET","POST","OPTIONS"],
    allow_headers=["*"],
)

# ── 型定義 ────────────────────────────────────────────────
ToolName = Literal["iching","tarot","lopan","shichu","meihua"]
AIModel  = Literal["claude","gemini","openai"]

class FortuneRunRequest(BaseModel):
    tool:      ToolName
    question:  str = Field(..., min_length=1, max_length=200)
    params:    dict = Field(default_factory=dict)
    timestamp: Optional[int] = None

class FortuneQueryRequest(BaseModel):
    tool:       ToolName
    raw_result: dict
    question:   str
    language:   str      = Field(default="ja")
    ai_model:   AIModel  = Field(default="claude",
                    description="使用するAIモデル: claude / gemini / openai")

class WuxingVector(BaseModel):
    wood:float=0.0; fire:float=0.0; earth:float=0.0
    metal:float=0.0; water:float=0.0

class FortuneRunResponse(BaseModel):
    tool:ToolName; timestamp:int; wuxing:WuxingVector
    raw_result:dict; summary:str; symbols:list[str]; time_context:dict

class FortuneQueryResponse(BaseModel):
    tool:ToolName; core:str; detail:str; action:str
    resonance:Optional[dict]=None
    ai_model_used:str=""

# ── レジストリ ───────────────────────────────────────────
_registry_cache: Optional[dict] = None

def load_registry() -> dict:
    global _registry_cache
    if _registry_cache: return _registry_cache
    for path in [ROOT/"core"/"registry_a.json",
                 ROOT/"fortune-core"/"docs"/"index.json",
                 ROOT/"fortune-registry"/"registry.json"]:
        if path.exists():
            with open(path, encoding="utf-8") as f:
                _registry_cache = json.load(f)
            return _registry_cache
    raise RuntimeError("registry_a.json が見つかりません")

# ── 時間コンテキスト ─────────────────────────────────────
TG = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
DZ = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]

def get_time_context(dt=None):
    dt = dt or datetime.now()
    y  = dt.year
    d  = (dt.date()-datetime(2024,1,1).date()).days
    return {
        "yearKanshi": TG[(y-4)%10]+DZ[(y-4)%12],
        "dayKanshi":  TG[((d%10)+10)%10]+DZ[((d%12)+12)%12],
        "monthKanshi":"?"+DZ[((dt.month-1+2)%12)],
        "junishi":    DZ[((d%12)+12)%12],
        "yuejian":    DZ[((dt.month-1+2)%12)],
        "rizhen":     DZ[((d%12)+12)%12],
        "kyusei":     ((11-(y%9))%9) or 9,
        "kanshi":     TG[(y-4)%10]+DZ[(y-4)%12],
    }

# ── ツール別ロジック ─────────────────────────────────────
def _run_iching(question, params, registry):
    try:
        from meihua.meihuaEngine import run as mr
        return {"engine":"meihua","result":mr(question,params)}
    except ImportError: pass
    now   = datetime.now()
    upper = ((now.year+now.month+now.day+now.hour)%8) or 8
    lower = ((upper+now.hour)%8) or 8
    dong  = ((now.year+now.month+now.day+now.hour)%6) or 6
    nm = ["","乾","兌","離","震","巽","坎","艮","坤"]
    id_ = ["","qian","dui","li","zhen","xun","kan","gen","kun"]
    entry = next((v for v in registry.get("hexagrams",{}).values()
                  if v.get("upper")==id_[upper] and v.get("lower")==id_[lower]),None)
    return {"engine":"iching_fallback","upperGua":nm[upper],"lowerGua":nm[lower],
            "dongYao":dong,
            "hexName":  entry["name_ja"] if entry else f"{nm[upper]}上/{nm[lower]}下",
            "hexCore":  entry["core"]    if entry else "卦を読み解いています。",
            "hexNumber":entry["number"]  if entry else 0}

def _run_tarot(question, params, registry):
    import random
    tarot = registry.get("tarot",{})
    if not tarot: raise HTTPException(500,"タロットデータがありません")
    drawn = random.sample(list(tarot.values()),min(3,len(tarot)))
    wx_acc = {k:0 for k in ["wood","fire","earth","metal","water"]}
    spread = []
    for i,card in enumerate(drawn):
        rev = random.random()<0.3
        spread.append({"position":["過去","現在","未来"][i],
            "card":card["name_ja"],"name_en":card["name_en"],
            "number":card["number"],"wuxing":card["wuxing"],
            "keywords":card["keywords"],"reversed":rev,"core":card["core"]})
        if card["wuxing"] in wx_acc: wx_acc[card["wuxing"]] += 1
    return {"engine":"tarot_major_arcana","spread":spread,"wuxing_raw":wx_acc}

def _run_shichu(question, params, registry):
    birth = params.get("birth_date","")
    if not birth: raise HTTPException(400,"birth_date (YYYY-MM-DD) が必要です")
    try:
        dt = datetime.strptime(birth,"%Y-%m-%d")
        return {"engine":"shichu_fallback","birth":birth,
                "yearKanshi":get_time_context(dt)["yearKanshi"]}
    except ValueError: raise HTTPException(400,"birth_date の形式が不正です")

def _run_lopan(question, params, registry):
    lopan = registry.get("lopan",{})
    ctx   = get_time_context()
    lucky = lopan.get("lucky_directions_by_kyusei",{}).get(str(ctx["kyusei"]),{})
    return {"engine":"lopan","kyusei":ctx["kyusei"],
            "best_dirs":lucky.get("best",[]),"avoid_dirs":lucky.get("avoid",[]),
            "note":f"今年の九星：{ctx['kyusei']}星　吉方位：{', '.join(lucky.get('best',[]))}"}

DISPATCH = {"iching":_run_iching,"meihua":_run_iching,
            "tarot":_run_tarot,"shichu":_run_shichu,"lopan":_run_lopan}

def calc_wuxing(tool, raw):
    v = {k:0.0 for k in ["wood","fire","earth","metal","water"]}
    if tool in ("iching","meihua"):
        bm = {"qian":"metal","dui":"metal","li":"fire","zhen":"wood",
              "xun":"wood","kan":"water","gen":"earth","kun":"earth"}
        nm = {"乾":"qian","兌":"dui","離":"li","震":"zhen",
              "巽":"xun","坎":"kan","艮":"gen","坤":"kun"}
        for k in ("upperGua","lowerGua"):
            wx = bm.get(nm.get(raw.get(k,""),""))
            if wx: v[wx] = min(1.0,v[wx]+0.4)
    elif tool=="tarot":
        t = sum(raw.get("wuxing_raw",{}).values()) or 1
        for k in v: v[k] = raw.get("wuxing_raw",{}).get(k,0)/t
    elif tool=="lopan":
        dm = {"N":"water","NE":"earth","E":"wood","SE":"wood",
              "S":"fire","SW":"earth","W":"metal","NW":"metal"}
        for d in raw.get("best_dirs",[]):
            wx = dm.get(d)
            if wx: v[wx] = min(1.0,v[wx]+0.35)
    t = sum(v.values()) or 1
    return WuxingVector(**{k:round(val/t,3) for k,val in v.items()})

# ── AI 読み解き（3モデル対応）────────────────────────────

SYSTEM_BASE = """あなたは東洋の伝統的な思想体系——易経・風水・陰陽五行——に精通した占術師です。
回答は必ず以下のJSON形式のみで返してください（前置き・マークダウン不要）:
{{"core":"核心メッセージ（50字以内）","detail":"詳細解釈（200字）","action":"推奨アクション（100字）",
"resonance":{{"suggestedTool":"iching|tarot|lopan のいずれか","reason":"理由（50字）"}}}}"""

def build_prompt(req: FortuneQueryRequest, tool_prompt: str) -> tuple[str, str]:
    system = SYSTEM_BASE + ("\n\n" + tool_prompt if tool_prompt else "")
    user   = f"質問: {req.question}\nツール: {req.tool}\n結果: {json.dumps(req.raw_result,ensure_ascii=False)}"
    return system, user

def parse_ai_response(text: str) -> dict:
    text = text.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"): text = text[4:]
    return json.loads(text.strip())

async def call_claude(system: str, user: str) -> tuple[dict, str]:
    if not ANTHROPIC_API_KEY:
        raise HTTPException(503,"ANTHROPIC_API_KEY が未設定です")
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    res    = client.messages.create(
        model="claude-sonnet-4-6", max_tokens=1000,
        system=system, messages=[{"role":"user","content":user}])
    return parse_ai_response(res.content[0].text), "claude-sonnet-4-6"

async def call_gemini(system: str, user: str) -> tuple[dict, str]:
    if not GEMINI_API_KEY:
        raise HTTPException(503,"GEMINI_API_KEY が未設定です")
    import urllib.request, urllib.error
    MODEL   = "gemini-2.0-flash"
    url     = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={GEMINI_API_KEY}"
    payload = json.dumps({
        "system_instruction": {"parts":[{"text":system}]},
        "contents": [{"parts":[{"text":user}]}],
        "generationConfig": {"temperature":0.7,"maxOutputTokens":1000},
    }).encode()
    req = urllib.request.Request(url, data=payload,
              headers={"Content-Type":"application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        text = data["candidates"][0]["content"]["parts"][0]["text"]
        return parse_ai_response(text), MODEL
    except urllib.error.HTTPError as e:
        raise HTTPException(502, f"Gemini API エラー: {e.code} {e.reason}")

async def call_openai(system: str, user: str) -> tuple[dict, str]:
    if not OPENAI_API_KEY:
        raise HTTPException(503,"OPENAI_API_KEY が未設定です")
    import urllib.request, urllib.error
    MODEL   = "gpt-4o-mini"
    url     = "https://api.openai.com/v1/chat/completions"
    payload = json.dumps({
        "model": MODEL,
        "messages": [
            {"role":"system","content":system},
            {"role":"user",  "content":user},
        ],
        "max_tokens": 1000,
        "temperature": 0.7,
        "response_format": {"type":"json_object"},
    }).encode()
    req = urllib.request.Request(url, data=payload, headers={
        "Content-Type":"application/json",
        "Authorization":f"Bearer {OPENAI_API_KEY}",
    }, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        text = data["choices"][0]["message"]["content"]
        return parse_ai_response(text), MODEL
    except urllib.error.HTTPError as e:
        raise HTTPException(502, f"OpenAI API エラー: {e.code} {e.reason}")

AI_CALLERS = {"claude":call_claude,"gemini":call_gemini,"openai":call_openai}

# ── エンドポイント ────────────────────────────────────────
@app.get("/fortune/health")
def health():
    return {
        "status": "ok", "version": "2.1.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tools":    list(DISPATCH.keys()),
        "ai_models": {
            "claude": bool(ANTHROPIC_API_KEY),
            "gemini": bool(GEMINI_API_KEY),
            "openai": bool(OPENAI_API_KEY),
        },
    }

@app.get("/fortune/tools")
def list_tools():
    return {"tools":[
        {"id":"iching","name":"梅花心易・六爻","status":"available"},
        {"id":"tarot", "name":"タロット",      "status":"available"},
        {"id":"shichu","name":"四柱推命",       "status":"available"},
        {"id":"lopan", "name":"風水・羅盤",     "status":"available"},
        {"id":"meihua","name":"梅花心易（詳細）","status":"available"},
    ]}

@app.post("/fortune/run", response_model=FortuneRunResponse)
def fortune_run(req: FortuneRunRequest):
    registry = load_registry()
    fn = DISPATCH.get(req.tool)
    if not fn: raise HTTPException(400,f"未対応ツール: {req.tool}")
    try:
        raw = fn(req.question, req.params, registry)
    except HTTPException: raise
    except Exception as e: raise HTTPException(500, str(e))
    wuxing   = calc_wuxing(req.tool, raw)
    time_ctx = get_time_context()
    ts       = req.timestamp or int(datetime.now().timestamp()*1000)
    bgmap    = {"乾":"☰","兌":"☱","離":"☲","震":"☳","巽":"☴","坎":"☵","艮":"☶","坤":"☷"}
    symbols: list[str] = []
    if req.tool in ("iching","meihua"):
        for k in ("upperGua","lowerGua"):
            g = raw.get(k,"")
            if g in bgmap: symbols.append(bgmap[g])
        if raw.get("hexName"): symbols.append(raw["hexName"])
    elif req.tool=="tarot":
        symbols = [s["card"] for s in raw.get("spread",[])]
    elif req.tool=="lopan":
        symbols = raw.get("best_dirs",[])
    summary = (raw.get("hexCore") or
               (raw["spread"][1]["core"] if raw.get("spread") else None) or
               raw.get("note") or "占断結果を生成しました。")
    return FortuneRunResponse(tool=req.tool,timestamp=ts,wuxing=wuxing,
        raw_result=raw,summary=summary,symbols=symbols,time_context=time_ctx)

@app.post("/fortune/query", response_model=FortuneQueryResponse)
async def fortune_query(req: FortuneQueryRequest):
    prompt_path = ROOT/"fortune-registry"/"prompts"/f"{req.tool}.json"
    tool_prompt = ""
    if prompt_path.exists():
        with open(prompt_path,encoding="utf-8") as f:
            tool_prompt = json.load(f).get("system","")

    system, user = build_prompt(req, tool_prompt)
    caller = AI_CALLERS.get(req.ai_model, call_claude)

    try:
        parsed, model_used = await caller(system, user)
    except HTTPException: raise
    except json.JSONDecodeError as e:
        raise HTTPException(500,f"JSON変換失敗: {e}")
    except Exception as e:
        raise HTTPException(500,f"AI API エラー: {e}")

    return FortuneQueryResponse(
        tool=req.tool, core=parsed.get("core",""),
        detail=parsed.get("detail",""), action=parsed.get("action",""),
        resonance=parsed.get("resonance"), ai_model_used=model_used)
