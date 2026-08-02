from __future__ import annotations

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

class HexagramResponse(HexagramBaseResponse):
    """
    易経卦情報（互換用）
    """

    changing_lines: list[int] = Field(
        default_factory=list
    )

    changed_number: int | None = None

    changed_name: str | None = None


class PrimaryHexagramResponse(HexagramBaseResponse):
    """
    本卦情報
    """

    upper: str | None = None

    lower: str | None = None

    judgement: str | None = None

    image: str | None = None


class ChangedHexagramResponse(HexagramBaseResponse):
    """
    之卦情報
    """

    pass


class ChangingLineResponse(BaseModel):
    """
    動爻情報
    """

    position: int

    value: int

    text: str | None = None


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

    lines: list[dict] = Field(
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
    "DivineRequest",
    "RootResponse",
    "MethodsResponse",
    "HexagramResponse",
    "PrimaryHexagramResponse",
    "ChangedHexagramResponse",
    "ChangingLineResponse",
    "InterpretationResponse",
    "FortuneResponse",
    "IChingResponse",
    "ErrorResponse",
    "VersionResponse",
    "HealthResponse",
    "SimulationRequest",
    "SimulationItem",
    "SimulationResponse",
    "RegistryInfoResponse",
]