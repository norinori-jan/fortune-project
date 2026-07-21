from __future__ import annotations

from typing import Any

from pydantic import BaseModel
from pydantic import Field


# ==========================================================
# Request Models
# ==========================================================

class DivineRequest(BaseModel):
    """
    易経占いリクエスト
    """

    question: str = Field(
        ...,
        description="相談内容",
        examples=["転職しても良いですか？"],
    )

    method: str = Field(
        default="coin",
        description="占法",
        examples=["coin"],
    )


# ==========================================================
# Response Models
# ==========================================================

class RootResponse(BaseModel):
    """
    APIルート
    """

    service: str

    engine: str

    status: str


class MethodsResponse(BaseModel):
    """
    利用可能な占法一覧
    """

    methods: list[str]


# ==========================================================
# Hexagram
# ==========================================================

class HexagramResponse(BaseModel):
    """
    卦情報
    """

    number: int

    name: str

    changing_lines: list[int]

    changed_number: int

    changed_name: str


# ==========================================================
# Interpretation
# ==========================================================

class InterpretationResponse(BaseModel):
    """
    解釈結果
    """

    mode: str

    title: str

    message: str

    lines: list[dict[str, Any]] = Field(
        default_factory=list
    )


# ==========================================================
# Fortune
# ==========================================================

class FortuneResponse(BaseModel):
    """
    易経占い結果
    """

    question: str

    method: str

    hexagram: HexagramResponse

    interpretation: InterpretationResponse


# ==========================================================
# Error
# ==========================================================

class ErrorResponse(BaseModel):
    """
    エラーレスポンス
    """

    error: str

    detail: str | None = None


# ==========================================================
# Version
# ==========================================================

class VersionResponse(BaseModel):
    """
    バージョン情報
    """

    name: str

    version: str

    api: str


# ==========================================================
# Health
# ==========================================================

class HealthResponse(BaseModel):
    """
    ヘルスチェック
    """

    status: str

    engine: str

    registry: str


# ==========================================================
# Simulation
# ==========================================================

class SimulationRequest(BaseModel):
    """
    シミュレーション要求
    """

    method: str = "coin"

    count: int = Field(
        default=1000,
        ge=1,
        le=100000,
    )


class SimulationItem(BaseModel):
    """
    卦ごとの集計
    """

    number: int

    name: str

    count: int

    percentage: float


class SimulationResponse(BaseModel):
    """
    シミュレーション結果
    """

    method: str

    count: int

    results: list[SimulationItem]


# ==========================================================
# Registry
# ==========================================================

class RegistryInfoResponse(BaseModel):
    """
    レジストリ情報
    """

    trigrams: int

    hexagrams: int

    judgements: int

    images: int

    yao: int


# ==========================================================
# __all__
# ==========================================================

__all__ = [
    "DivineRequest",
    "RootResponse",
    "MethodsResponse",
    "HexagramResponse",
    "InterpretationResponse",
    "FortuneResponse",
    "ErrorResponse",
    "VersionResponse",
    "HealthResponse",
    "SimulationRequest",
    "SimulationItem",
    "SimulationResponse",
    "RegistryInfoResponse",
]