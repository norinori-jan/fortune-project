import sys
sys.path.append("C:/Users/norin/fortune-project")

from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

# -----------------------------
# Loader（fortune-registry）
# -----------------------------
from fortune_registry.loader import RegistryLoader

# -----------------------------
# 命式エンジン
# -----------------------------
from fortune_core.shichu.engine import Engine

# AI レイヤー
from fortune_core.ai.explain import AIExplain
from fortune_core.ai.reading import AIReading
from fortune_core.ai.qa import AIQA


# -----------------------------
# FastAPI アプリ
# -----------------------------
app = FastAPI()


# -----------------------------
# RegistryLoader の初期化
# -----------------------------
registry_loader = RegistryLoader(
    base_path="C:/Users/norin/fortune-project/fortune-registry"
)

# -----------------------------
# Engine の初期化
# -----------------------------
engine = Engine(
    registry_loader=registry_loader,
    solar_terms_json_path="C:/Users/norin/fortune-project/fortune-registry/shichu/solar_terms.json"
)


# -----------------------------
# AI レイヤー
# -----------------------------
ai_explain = AIExplain()
ai_reading = AIReading()
ai_qa = AIQA(engine)


# -----------------------------
# リクエストモデル
# -----------------------------
class GenerateRequest(BaseModel):
    birth: str
    gender: str
    longitude: float | None = None


class QARequest(BaseModel):
    birth: str
    gender: str
    question: str


# -----------------------------
# /generate 命式生成
# -----------------------------
@app.post("/generate")
def generate(req: GenerateRequest):
    birth_dt = datetime.fromisoformat(req.birth)
    chart = engine.generate(birth_dt, req.gender, req.longitude)
    return chart.dict()


# -----------------------------
# /explain 命式解説
# -----------------------------
@app.post("/explain")
def explain(req: GenerateRequest):
    birth_dt = datetime.fromisoformat(req.birth)
    chart = engine.generate(birth_dt, req.gender, req.longitude)
    return {"explanation": ai_explain.explain_all(chart)}


# -----------------------------
# /reading 総合鑑定
# -----------------------------
@app.post("/reading")
def reading(req: GenerateRequest):
    birth_dt = datetime.fromisoformat(req.birth)
    chart = engine.generate(birth_dt, req.gender, req.longitude)

    today = datetime.now()
    text = ai_reading.full_reading(
        chart,
        engine,
        target_year=today.year,
        target_month=today.month,
        target_date=today
    )
    return {"reading": text}


# -----------------------------
# /qa 質疑応答
# -----------------------------
@app.post("/qa")
def qa(req: QARequest):
    birth_dt = datetime.fromisoformat(req.birth)
    chart = engine.generate(birth_dt, req.gender)

    today = datetime.now()
    answer = ai_qa.answer(chart, req.question, today)
    return {"answer": answer}
