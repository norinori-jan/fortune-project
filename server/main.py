from __future__ import annotations

from fastapi import FastAPI

from fortune_core.api import (
    IChingRequest,
    api,
)

from server.models import (
    DivineRequest,
    FortuneResponse,
    MethodsResponse,
    RootResponse,
    HexagramResponse,
    InterpretationResponse,
)

app = FastAPI(
    title="Fortune Project API",
    version="2.0.0",
)
# ==========================================================
# Health Check
# ==========================================================

@app.get("/health")
def health() -> dict:
    """
    API health check
    """

    return {
        "status": "ok",
        "service": "fortune-api",
        "modules": {
            "iching": True,
        },
    }

# ==========================================================
# Root
# ==========================================================

@app.get(
    "/",
    response_model=RootResponse,
)
def root() -> RootResponse:
    """
    API動作確認
    """

    return RootResponse(
        service="fortune-project",
        engine="I Ching",
        status="ok",
    )


# ==========================================================
# Methods
# ==========================================================

@app.get(
    "/methods",
    response_model=MethodsResponse,
)
def methods() -> MethodsResponse:
    """
    利用可能な占法一覧
    """

    return MethodsResponse(
        methods=[
            "coin",
            "simple_yarrow",
            "traditional_yarrow",
        ]
    )


# ==========================================================
# I Ching
# ==========================================================

@app.post(
    "/iching",
    response_model=FortuneResponse,
)
def divine(
    request: DivineRequest,
) -> FortuneResponse:
    """
    易経占い
    """

    result = api.divine(
        IChingRequest(
            question=request.question,
            method=request.method,
        )
    )

    return FortuneResponse(
        question=result.question,
        method=result.method,
        hexagram=HexagramResponse(
            number=result.hexagram.hexagram_number,
            name=result.hexagram.hexagram_name,
            changing_lines=result.hexagram.changing_lines,
            changed_number=result.hexagram.changed_hexagram_number,
            changed_name=result.hexagram.changed_hexagram_name,
        ),
        interpretation=InterpretationResponse(
            mode=result.interpretation.mode,
            title=result.interpretation.title,
            message=result.interpretation.message,
            lines=result.interpretation.lines,
        ),
    )