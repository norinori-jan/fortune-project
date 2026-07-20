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

