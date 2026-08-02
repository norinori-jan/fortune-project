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
        examples=[
            "転職しても良いですか？"
        ],
    )

    method: str = Field(
        default="coin",
        description="占法",
        examples=[
            "coin"
        ],
    )


# ==========================================================
# Common
# ==========================================================


class HexagramBaseResponse(BaseModel):
    """
    卦基本情報
    """

    number: int

    name: str



# ==========================================================
# Hexagram
# ==========================================================


class HexagramResponse(
    HexagramBaseResponse
):
    """
    易経卦情報（互換用）
    """

    lines: list[Any] = Field(
        default_factory=list
    )

    changed_number: int | None = None

    changed_name: str | None = None



class PrimaryHexagramResponse(
    HexagramBaseResponse
):
    """
    本卦情報

    registry の judgement/image
    は辞書構造で保持する。
    """

    upper: str = Field(
        ...,
        description="上卦",
    )

    lower: str = Field(
        ...,
        description="下卦",
    )

    judgement: Any = Field(
        default_factory=dict,
        description="卦辞",
    )

    image: Any = Field(
        default_factory=dict,
        description="象伝",
    )



class ChangedHexagramResponse(
    HexagramBaseResponse
):
    """
    之卦情報
    """

    pass

# ==========================================================
# Changing Line Interpretation
# ==========================================================


class ChangingLineInterpretationResponse(BaseModel):
    """
    変爻解釈
    """

    line: int

    original: str

    translation: str

    meaning: str

    advice: str

    keywords: list[str] = Field(
        default_factory=list
    )



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

    lines: list[ChangingLineInterpretationResponse] = Field(
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



class IChingResponse(BaseModel):
    """
    新しい易経APIレスポンス形式

    frontend向け
    """

    question: str

    method: str

    primary: PrimaryHexagramResponse


    changing_lines: list[ChangingLineResponse] = Field(
        default_factory=list
    )


    changed: ChangedHexagramResponse | None = None


    interpretation: InterpretationResponse
# ==========================================================
# Changing Line
# ==========================================================


class ChangingLineResponse(BaseModel):
    """
    変爻レスポンス
    """

    line: int = Field(
        ...,
        description="変爻位置(1〜6)",
    )

    original: str = Field(
        ...,
        description="原文",
    )

    translation: str = Field(
        ...,
        description="現代語訳",
    )

    meaning: str = Field(
        ...,
        description="意味",
    )

    advice: str = Field(
        ...,
        description="助言",
    )

    keywords: list[str] = Field(
        default_factory=list,
        description="キーワード",
    )
# ==========================================================
# Root
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

    service: str

    modules: dict[str, bool]



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

    # Request
    "DivineRequest",


    # Hexagram
    "HexagramBaseResponse",
    "HexagramResponse",
    "PrimaryHexagramResponse",
    "ChangingLineResponse",

    "ChangingLineInterpretationResponse",

    
    # Interpretation
    "InterpretationResponse",


    # Fortune
    "FortuneResponse",
    "IChingResponse",


    # Root / Methods
    "RootResponse",
    "MethodsResponse",


    # Error
    "ErrorResponse",


    # Version / Health
    "VersionResponse",
    "HealthResponse",


    # Simulation
    "SimulationRequest",
    "SimulationItem",
    "SimulationResponse",


    # Registry
    "RegistryInfoResponse",

]