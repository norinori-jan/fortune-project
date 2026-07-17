# app/schemas.py

from typing import Any

from pydantic import BaseModel, Field


# ============================================================
# 四柱推命
# ============================================================

class ShichuRequest(BaseModel):
    """
    四柱推命鑑定API入力
    """

    year: int = Field(..., ge=1800, le=2200)
    month: int = Field(..., ge=1, le=12)
    day: int = Field(..., ge=1, le=31)

    hour: int = Field(..., ge=0, le=23)
    minute: int = Field(..., ge=0, le=59)

    gender: str = Field(
        ...,
        description="男 または 女",
    )

    longitude: float | None = Field(
        default=None,
        description="出生地経度（東経＋ 西経－）",
    )


# ============================================================
# 易経
# ============================================================

class IChingRequest(BaseModel):
    """
    易経占い入力
    """

    numbers: list[int] = Field(
        ...,
        min_length=6,
        max_length=6,
        description="六爻（6・7・8・9）",
    )


# ============================================================
# タロット
# ============================================================

class TarotRequest(BaseModel):
    """
    タロット占い入力
    """

    spread: str = Field(
        default="single",
        description="single / three / celtic",
    )

    cards: list[int] = Field(
        ...,
        description="カード番号",
    )

    reversed: list[bool] = Field(
        default_factory=list,
        description="逆位置フラグ",
    )


# ============================================================
# 共通レスポンス
# ============================================================

class PaperReportResponse(BaseModel):
    """
    四柱推命鑑定書
    """

    chart: Any

    element_strength: Any

    kakukyoku: Any

    yojin: Any

    house_gods: Any

    combinations: Any

    taiun: Any

    ryunen: Any

    ryugetsu: Any

    ryunichi: Any

    ai_reading: Any

    class Config:
        arbitrary_types_allowed = True


class IChingResponse(BaseModel):
    """
    易経APIレスポンス
    """

    result: Any

    class Config:
        arbitrary_types_allowed = True


class TarotResponse(BaseModel):
    """
    タロットAPIレスポンス
    """

    result: Any

    class Config:
        arbitrary_types_allowed = True