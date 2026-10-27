from __future__ import annotations
from pydantic import BaseModel, Field
class TarotRequest(BaseModel):
    question: str = Field(min_length=1)
    orientation: str = "auto"
class MeihuaRequest(BaseModel):
    question: str = Field(min_length=1)
class ElementRequest(BaseModel):
    text: str = Field(min_length=1)
class ShichuRequest(BaseModel):
    birth_date: str = Field(
        pattern=r"^\d{4}-\d{2}-\d{2}$"
    )
class HistoryRequest(BaseModel):
    limit: int = Field(default=20, ge=1, le=100)