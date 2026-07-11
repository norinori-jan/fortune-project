# api.py
# ======
# fortune-core FastAPI サーバ�E
#
# 起動コマンチE
#     uvicorn src.fortune_core.api:app --reload --host 0.0.0.0 --port 8000
#
# エンド�EインチE
#     GET  /                      - スチE�Eタス確誁E
#     GET  /api/divine            - 相諁E�E容を�E劁EↁE占術判宁E+ タロチE��展開
#     GET  /api/docs              - Swagger UI

import time
from datetime import datetime
from typing import Optional, List, Dict

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# 既存�Eコアコンポ�Eネントをインポ�EチE
from fortune_core.divination_entry import DivineEntryEngine
from fortune_core.tarot_engine import TarotEngine
from fortune_core.report_generator import ReportGenerator, ReadingReport

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FastApp 初期匁E
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

app = FastAPI(
    title="🔮 Fortune Core API",
    description="相諁E�E容の解析からタロチE��展開までを一允E��琁E��る占ぁE��チE��エンドAPI",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# CORS 設定（フロントエンド�Eモバイルアプリから直接アクセス可能�E�E
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# エンジンの初期化（シングルトン�E�E
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

entry_engine = DivineEntryEngine()
tarot_engine = TarotEngine()
report_generator = ReportGenerator()

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Pydantic モチE��
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

class AnalysisResponse(BaseModel):
    """相諁E�E容の刁E��結果"""
    query: str
    concern_type: str
    recommended_spread: str
    confidence_score: float
    reasoning: str
    guidance: str


class CardPosition(BaseModel):
    """カード位置チE�Eタ"""
    position_label: str
    position_index: int
    card_name: str
    element: str
    is_reversed: bool
    meaning: str


class DivinationResponse(BaseModel):
    """完�Eな鑑定結果"""
    success: bool
    reading_id: str
    timestamp: str
    analysis: AnalysisResponse
    positions: List[CardPosition]
    element_distribution: Dict[str, int]
    guidance_summary: str


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ヘルスチェチE��
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get("/")
def read_root():
    """スチE�Eタス確誁E""
    return {
        "status": "online",
        "message": "Welcome to Fortune Core API. Let's divine your destiny.",
        "api_version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
def health_check():
    """ヘルスチェチE��"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "engines": {
            "entry": "ready",
            "tarot": "ready",
            "report": "ready"
        }
    }


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# メイン API エンド�EインチE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get("/api/divine", response_model=DivinationResponse)
def divine(
    query: str = Query(
        ...,
        description="ユーザーの相諁E�E容を�E力してください",
        min_length=1,
        max_length=500
    ),
    user_seed: Optional[int] = Query(
        None,
        description="シンクロニシチE��シード（ミリ秒タイムスタンプ）。省略時�Eサーバ�E側で生�E、E
    ),
    save_report: bool = Query(
        False,
        description="JSON/HTMLレポ�Eトを保存するか�E�Erue = 保存！E
    )
):
    """
    【メイン占いAPI、E
    
    相諁E�E容�E��E然言語）を受け取り、以下を一撁E��実衁E
    1. 占ぁE�E入り口�E�相諁E�E容を�E動解极E
    2. 占術判定：最適な占術を推奨�E�信度スコア付き�E�E
    3. タロチE��展開�E�ケルト十字スプレチE��実衁E
    4. レポ�Eト生成：JSON/HTML�E�オプション保存！E
    
    Returns:
        DivinationResponse: 完�Eな鑑定結果�E��E析＋占ぁE��果�E�要素刁E���E�E
    """
    try:
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # STEP 1: 相諁E�E容の刁E�� ↁE占術推奨
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        entry = entry_engine.create_entry(query)
        recommendation = entry.recommendation

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # STEP 2: シンクロニシチE��シード決宁E
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        if user_seed is None:
            user_seed = int(time.time() * 1000)

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # STEP 3: タロチE��展開
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # �E�現在はタロチE��・ケルト十字をチE��ォルト！E
        if recommendation and getattr(recommendation, "divination_type", ""):
            div_type = recommendation.divination_type
        else:
            div_type = "tarot"

        if "tarot" in div_type.lower():
            reading_result = tarot_engine.draw_celtic_cross(
                user_seed=user_seed,
                query=query
            )
        else:
            # フォールバック�E�他�E占術�Eまだ未実裁E��E
            reading_result = tarot_engine.draw_celtic_cross(
                user_seed=user_seed,
                query=query
            )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # STEP 4: ポジション惁E��をAPI形式に変換�E�堁E��化！E
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        positions_api: List[CardPosition] = []
        element_dist: Dict[str, int] = {}

        raw_positions = reading_result.get("positions", {}) if isinstance(reading_result, dict) else {}

        # 安定した頁E��で返すため position_index でソート（存在しなぁE��合�Eキー頁E��E
        try:
            sorted_items = sorted(
                raw_positions.items(),
                key=lambda kv: int(kv[1].get("position_index", 0)) if isinstance(kv[1], dict) else 0
            )
        except Exception:
            sorted_items = list(raw_positions.items())

        for pos_key, pos_data in sorted_items:
            if not isinstance(pos_data, dict):
                pos_data = {}

            card = pos_data.get("card", {}) or {}
            element = card.get("element", "unknown") or "unknown"
            is_reversed = bool(pos_data.get("is_reversed", False))

            # 要素刁E��E��ウンチE
            element_dist[element] = element_dist.get(element, 0) + 1

            # 解釈文を選抁E
            meaning_key = "meaning_reversed" if is_reversed else "meaning_upright"
            meaning = card.get(meaning_key, "") or ""

            # position_index を�E示皁E�� int にする�E�Eone 対策！E
            try:
                position_index = int(pos_data.get("position_index", 0))
            except (TypeError, ValueError):
                position_index = 0

            positions_api.append(
                CardPosition(
                    position_label=str(pos_data.get("position_label", "")) or "",
                    position_index=position_index,
                    card_name=str(card.get("name", "Unknown")) or "Unknown",
                    element=str(element),
                    is_reversed=is_reversed,
                    meaning=str(meaning)
                )
            )

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # STEP 5: レポ�Eト生成（オプション保存！E
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        reading_id = f"reading_{user_seed}"

        if save_report:
            report = ReadingReport(
                reading_id=reading_id,
                query_text=query,
                timestamp=datetime.now().isoformat(),
                divination_type=div_type,
                positions=raw_positions,
                element_distribution=element_dist,
                user_seed=user_seed,
            )
            try:
                report_generator.export_formats(report, formats=("json", "html"))
            except Exception as e:
                # レポ�Eト保存に失敗してめEPI応答�E継綁E
                print(f"Warning: Report save failed - {e}")

        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
        # STEP 6: API応答を構篁E
        # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        guidance_text = getattr(recommendation, "user_guidance", "") if recommendation else ""
        guidance_summary = (
            f"最適な占術�E【{div_type}】です、En"
            f"{(guidance_text or '')[:200]}..."
        )

        analysis_obj = AnalysisResponse(
            query=query,
            concern_type=getattr(entry, "concern_type", "") if entry else "",
            recommended_spread=div_type,
            confidence_score=float(getattr(recommendation, "confidence", 0.0)) if recommendation else 0.0,
            reasoning=getattr(recommendation, "reasoning", "") if recommendation else "",
            guidance=guidance_text or "",
        )

        return DivinationResponse(
            success=True,
            reading_id=reading_id,
            timestamp=datetime.now().isoformat(),
            analysis=analysis_obj,
            positions=positions_api,
            element_distribution=element_dist,
            guidance_summary=guidance_summary,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Divination failed: {str(e)}")


@app.get("/api/analysis")
def analyze_only(
    query: str = Query(
        ...,
        description="相諁E�E容を�E劁E,
        min_length=1,
        max_length=500
    )
):
    """
    相諁E�E容の刁E��のみ実行（タロチE��展開なし！E

    ユースケース�E�E
    - UI で推奨占術を先に表示して、ユーザーに確認してからタロチE��展開
    - レイチE��シ改喁E���E析だけなら高速！E
    """
    try:
        entry = entry_engine.create_entry(query)
        recommendation = entry.recommendation

        return {
            "success": True,
            "query": query,
            "concern_type": getattr(entry, "concern_type", "") if entry else "",
            "recommended_spread": getattr(recommendation, "divination_type", "") if recommendation else "",
            "confidence_score": float(getattr(recommendation, "confidence", 0.0)) if recommendation else 0.0,
            "reasoning": getattr(recommendation, "reasoning", "") if recommendation else "",
            "guidance": getattr(recommendation, "user_guidance", "") if recommendation else "",
            "follow_up_questions": entry_engine.suggest_follow_up_questions(entry)[:3] if entry else [],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# メタ惁E��
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.get("/api/info")
def api_info():
    """API 惁E��とエンド�Eイント一覧"""
    return {
        "api_name": "Fortune Core API",
        "version": "1.0.0",
        "description": "AI-powered divination backend with tarot, feng shui, and more",
        "endpoints": {
            "health": {
                "method": "GET",
                "path": "/api/health",
                "description": "ヘルスチェチE��"
            },
            "main_divine": {
                "method": "GET",
                "path": "/api/divine",
                "params": ["query", "user_seed (optional)", "save_report (optional)"],
                "description": "相諁E�E容 ↁE占術判宁E+ タロチE��展開�E�メインAPI�E�E
            },
            "analyze_only": {
                "method": "GET",
                "path": "/api/analysis",
                "params": ["query"],
                "description": "相諁E�E容の刁E��のみ�E�軽量！E
            },
            "docs": {
                "method": "GET",
                "path": "/api/docs",
                "description": "Swagger UI�E�インタラクチE��ブドキュメント！E
            }
        },
        "examples": {
            "divine": "/api/divine?query=今�EプロジェクトをどぁE��めるべきか�E�Esave_report=true",
            "analysis": "/api/analysis?query=彼との関係�E今後どぁE��りますか�E�E
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
